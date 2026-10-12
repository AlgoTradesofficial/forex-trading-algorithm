from AlgorithmImports import *
from datetime import timedelta


class ForexStrategySimulator(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2025, 7, 1)
        self.set_end_date(2026, 6, 1)
        self.set_cash(10000)
        self.set_time_zone("UTC")

        self.starting_equity = 10000.0
        self.sim_equity = 10000.0
        self.risk_percent = 10.0
        self.reward_risk = 0.5
        self.sl_buffer = 0.3

        self.ny_start, self.ny_end = 1, 9
        self.asia_start, self.asia_end = 12, 20

        security = self.add_forex("GBPUSD", Resolution.MINUTE, Market.OANDA)
        self.symbol = security.symbol

        self.consolidator = QuoteBarConsolidator(timedelta(minutes=5))
        self.consolidator.data_consolidated += self.on_five_minute_bar
        self.subscription_manager.add_consolidator(self.symbol, self.consolidator)

        self.bars = []

        self.was_in_ny = False
        self.was_in_asia = False
        self.ny_high = None
        self.ny_low = None
        self.trade_taken = False

        self.bullish_sweep_found = False
        self.bearish_sweep_found = False
        self.sweep_low = None
        self.sweep_high = None
        self.sweep_low_range = None
        self.sweep_high_range = None

        self.previous_swing_high = None
        self.previous_swing_low = None
        self.lower_high = None
        self.higher_low = None
        self.bullish_structure_broken = False
        self.bearish_structure_broken = False

        self.bullish_active = False
        self.bullish_touched = False
        self.bullish_top = None
        self.bullish_bottom = None

        self.bearish_active = False
        self.bearish_touched = False
        self.bearish_top = None
        self.bearish_bottom = None

        self.position = None

        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.gross_profit = 0.0
        self.gross_loss = 0.0
        self.peak_equity = self.starting_equity
        self.max_drawdown_pct = 0.0
        self.max_drawdown_money = 0.0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.max_consecutive_wins = 0
        self.max_consecutive_losses = 0
        self.long_trades = 0
        self.short_trades = 0

    def on_five_minute_bar(self, sender, bar):
        o = float(bar.open)
        h = float(bar.high)
        l = float(bar.low)
        c = float(bar.close)

        strategy_time = self.time + timedelta(hours=12)

        if self.position is not None:
            self.check_position(o, h, l, c, strategy_time)

        self.bars.append({"open": o, "high": h, "low": l, "close": c})

        if len(self.bars) < 3:
            self.update_session_memory(strategy_time)
            return

        if len(self.bars) > 10:
            self.bars.pop(0)

        current = self.bars[-1]
        previous = self.bars[-2]
        two_back = self.bars[-3]

        hour = strategy_time.hour
        in_ny = self.ny_start <= hour < self.ny_end
        in_asia = self.asia_start <= hour < self.asia_end

        new_ny = in_ny and not self.was_in_ny
        new_asia = in_asia and not self.was_in_asia

        if new_ny:
            self.ny_high = h
            self.ny_low = l

        if in_ny:
            if self.ny_high is None:
                self.ny_high = h
                self.ny_low = l
            else:
                self.ny_high = max(self.ny_high, h)
                self.ny_low = min(self.ny_low, l)

        if new_asia:
            self.trade_taken = False

            self.bullish_sweep_found = False
            self.bearish_sweep_found = False
            self.sweep_low = None
            self.sweep_high = None
            self.sweep_low_range = None
            self.sweep_high_range = None

            self.previous_swing_high = None
            self.previous_swing_low = None
            self.lower_high = None
            self.higher_low = None
            self.bullish_structure_broken = False
            self.bearish_structure_broken = False

            self.bullish_active = False
            self.bullish_touched = False
            self.bearish_active = False
            self.bearish_touched = False

        if in_asia and self.ny_low is not None:
            if not self.bullish_sweep_found and l < self.ny_low:
                self.bullish_sweep_found = True
                self.sweep_low = l
                self.sweep_low_range = h - l
            elif self.bullish_sweep_found and self.sweep_low is not None and l < self.sweep_low:
                self.sweep_low = l
                self.sweep_low_range = h - l

        if in_asia and self.ny_high is not None:
            if not self.bearish_sweep_found and h > self.ny_high:
                self.bearish_sweep_found = True
                self.sweep_high = h
                self.sweep_high_range = h - l
            elif self.bearish_sweep_found and self.sweep_high is not None and h > self.sweep_high:
                self.sweep_high = h
                self.sweep_high_range = h - l

        swing_high = (
            previous["high"] > two_back["high"]
            and previous["high"] > current["high"]
        )

        swing_low = (
            previous["low"] < two_back["low"]
            and previous["low"] < current["low"]
        )

        if in_asia and swing_high:
            swing_value = previous["high"]
            if self.previous_swing_high is not None and swing_value < self.previous_swing_high:
                self.lower_high = swing_value
            self.previous_swing_high = swing_value

        if in_asia and swing_low:
            swing_value = previous["low"]
            if self.previous_swing_low is not None and swing_value > self.previous_swing_low:
                self.higher_low = swing_value
            self.previous_swing_low = swing_value

        if (
            in_asia
            and self.bullish_sweep_found
            and not self.bullish_structure_broken
            and self.lower_high is not None
            and h > self.lower_high
        ):
            self.bullish_structure_broken = True

        if (
            in_asia
            and self.bearish_sweep_found
            and not self.bearish_structure_broken
            and self.higher_low is not None
            and l < self.higher_low
        ):
            self.bearish_structure_broken = True

        bullish_fvg = current["low"] > two_back["high"]
        bearish_fvg = current["high"] < two_back["low"]

        if (
            in_asia
            and self.bullish_structure_broken
            and not self.trade_taken
            and bullish_fvg
        ):
            self.bullish_top = current["low"]
            self.bullish_bottom = two_back["high"]
            self.bullish_active = True
            self.bullish_touched = False

        if (
            in_asia
            and self.bearish_structure_broken
            and not self.trade_taken
            and bearish_fvg
        ):
            self.bearish_top = two_back["low"]
            self.bearish_bottom = current["high"]
            self.bearish_active = True
            self.bearish_touched = False

        bullish_entry = False
        bearish_entry = False

        if self.bullish_active:
            entered = l <= self.bullish_top and h >= self.bullish_bottom
            invalidated = c < self.bullish_bottom

            if entered:
                self.bullish_touched = True

            if invalidated:
                self.bullish_active = False
                self.bullish_touched = False
            elif self.bullish_touched and c > self.bullish_top and c > o:
                bullish_entry = True
                self.bullish_active = False

        if self.bearish_active:
            entered = h >= self.bearish_bottom and l <= self.bearish_top
            invalidated = c > self.bearish_top

            if entered:
                self.bearish_touched = True

            if invalidated:
                self.bearish_active = False
                self.bearish_touched = False
            elif self.bearish_touched and c < self.bearish_bottom and c < o:
                bearish_entry = True
                self.bearish_active = False

        if (
            bullish_entry
            and not self.trade_taken
            and self.position is None
            and self.sweep_low is not None
            and self.sweep_low_range is not None
        ):
            entry = c
            stop = self.sweep_low - self.sweep_low_range * self.sl_buffer
            risk_per_unit = entry - stop

            if risk_per_unit > 0:
                risk_money = self.sim_equity * self.risk_percent / 100
                size = risk_money / risk_per_unit
                target = entry + risk_per_unit * self.reward_risk

                self.position = {
                    "side": "LONG",
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "size": size
                }

                self.trade_taken = True
                self.long_trades += 1

        elif (
            bearish_entry
            and not self.trade_taken
            and self.position is None
            and self.sweep_high is not None
            and self.sweep_high_range is not None
        ):
            entry = c
            stop = self.sweep_high + self.sweep_high_range * self.sl_buffer
            risk_per_unit = stop - entry

            if risk_per_unit > 0:
                risk_money = self.sim_equity * self.risk_percent / 100
                size = risk_money / risk_per_unit
                target = entry - risk_per_unit * self.reward_risk

                self.position = {
                    "side": "SHORT",
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "size": size
                }

                self.trade_taken = True
                self.short_trades += 1

        self.was_in_ny = in_ny
        self.was_in_asia = in_asia

    def check_position(self, o, h, l, c, strategy_time):
        p = self.position
        if p is None:
            return

        if p["side"] == "LONG":
            stop_hit = l <= p["stop"]
            target_hit = h >= p["target"]

            if stop_hit and target_hit:
                result = self.resolve_same_bar("LONG", o, h, l)
                self.close_position(
                    p["target"] if result == "TARGET" else p["stop"],
                    result
                )
            elif stop_hit:
                self.close_position(p["stop"], "STOP")
            elif target_hit:
                self.close_position(p["target"], "TARGET")

        else:
            stop_hit = h >= p["stop"]
            target_hit = l <= p["target"]

            if stop_hit and target_hit:
                result = self.resolve_same_bar("SHORT", o, h, l)
                self.close_position(
                    p["target"] if result == "TARGET" else p["stop"],
                    result
                )
            elif stop_hit:
                self.close_position(p["stop"], "STOP")
            elif target_hit:
                self.close_position(p["target"], "TARGET")

    def resolve_same_bar(self, side, o, h, l):
        high_first = abs(h - o) < abs(o - l)

        if side == "LONG":
            return "TARGET" if high_first else "STOP"

        return "STOP" if high_first else "TARGET"

    def close_position(self, exit_price, reason):
        p = self.position
        if p is None:
            return

        if p["side"] == "LONG":
            pnl = (exit_price - p["entry"]) * p["size"]
        else:
            pnl = (p["entry"] - exit_price) * p["size"]

        self.sim_equity += pnl
        self.total_trades += 1

        if pnl > 0:
            self.wins += 1
            self.gross_profit += pnl
            self.consecutive_wins += 1
            self.consecutive_losses = 0
            self.max_consecutive_wins = max(
                self.max_consecutive_wins,
                self.consecutive_wins
            )
        else:
            self.losses += 1
            self.gross_loss += abs(pnl)
            self.consecutive_losses += 1
            self.consecutive_wins = 0
            self.max_consecutive_losses = max(
                self.max_consecutive_losses,
                self.consecutive_losses
            )

        if self.sim_equity > self.peak_equity:
            self.peak_equity = self.sim_equity

        dd_money = self.peak_equity - self.sim_equity
        dd_pct = (
            dd_money / self.peak_equity * 100
            if self.peak_equity > 0 else 0
        )

        self.max_drawdown_money = max(self.max_drawdown_money, dd_money)
        self.max_drawdown_pct = max(self.max_drawdown_pct, dd_pct)

        self.plot("Simulated Equity", "Equity", self.sim_equity)
        self.position = None

    def update_session_memory(self, strategy_time):
        hour = strategy_time.hour
        self.was_in_ny = self.ny_start <= hour < self.ny_end
        self.was_in_asia = self.asia_start <= hour < self.asia_end

    def on_end_of_algorithm(self):
        win_rate = (
            self.wins / self.total_trades * 100
            if self.total_trades > 0 else 0
        )

        if self.gross_loss > 0:
            pf = self.gross_profit / self.gross_loss
            pf_text = f"{pf:.3f}"
        elif self.gross_profit > 0:
            pf_text = "Infinite"
        else:
            pf_text = "0"

        sim_return = (
            self.sim_equity / self.starting_equity - 1
        ) * 100

        self.set_runtime_statistic("Sim Equity", f"${self.sim_equity:.2f}")
        self.set_runtime_statistic("Sim Return", f"{sim_return:.2f}%")
        self.set_runtime_statistic("Sim Trades", str(self.total_trades))
        self.set_runtime_statistic("Wins", str(self.wins))
        self.set_runtime_statistic("Losses", str(self.losses))
        self.set_runtime_statistic("Win Rate", f"{win_rate:.2f}%")
        self.set_runtime_statistic("Profit Factor", pf_text)
        self.set_runtime_statistic(
            "Max Drawdown",
            f"{self.max_drawdown_pct:.2f}%"
        )
        self.set_runtime_statistic(
            "Max DD $",
            f"${self.max_drawdown_money:.2f}"
        )
        self.set_runtime_statistic("Long Trades", str(self.long_trades))
        self.set_runtime_statistic("Short Trades", str(self.short_trades))
