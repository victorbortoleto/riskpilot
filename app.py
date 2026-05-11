import streamlit as st
        daily_remaining = max_daily_loss - abs(daily_worst)
        max_dd_remaining = max_drawdown_limit - abs(metrics["max_drawdown"])

        prop1, prop2, prop3 = st.columns(3)
        with prop1:
            st.markdown(f'<div class="prop-card"><div class="metric-label">{t["target_distance"]}</div><div class="metric-value neutral">{money(remaining_target)}</div><div class="metric-help">{t["remaining_to_goal"]}</div></div>', unsafe_allow_html=True)
        with prop2:
            status = "negative" if daily_remaining < 0 else "neutral"
            st.markdown(f'<div class="prop-card"><div class="metric-label">{t["daily_dd_remaining"]}</div><div class="metric-value {status}">{money(daily_remaining)}</div><div class="metric-help">{t["daily_limit_margin"]}</div></div>', unsafe_allow_html=True)
        with prop3:
            status = "negative" if max_dd_remaining < 0 else "neutral"
            st.markdown(f'<div class="prop-card"><div class="metric-label">{t["max_dd_remaining"]}</div><div class="metric-value {status}">{money(max_dd_remaining)}</div><div class="metric-help">{t["max_dd_margin"]}</div></div>', unsafe_allow_html=True)

        section(t["equity_curve"])
        fig_equity = px.line(filtered_df, x="date", y="equity", title="Equity Curve")
        fig_equity.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_equity, use_container_width=True)

        section(t["drawdown"])
        fig_dd = px.area(filtered_df, x="date", y="drawdown", title="Drawdown")
        fig_dd.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_dd, use_container_width=True)

        section(t["daily_result"])
        daily_pnl = filtered_df.groupby("day")["net_pnl"].sum().reset_index()
        fig_daily = px.bar(daily_pnl, x="day", y="net_pnl", title="Daily P&L")
        fig_daily.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_daily, use_container_width=True)

        section(t["hour_result"])
        hourly = filtered_df.groupby("hour")["net_pnl"].sum().reset_index()
        fig_hour = px.bar(hourly, x="hour", y="net_pnl", title="Result by Hour")
        fig_hour.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_hour, use_container_width=True)

        section(t["weekday_result"])
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = filtered_df.groupby("weekday")["net_pnl"].sum().reset_index()
        weekday["weekday"] = pd.Categorical(weekday["weekday"], categories=weekday_order, ordered=True)
        weekday = weekday.sort_values("weekday")
        fig_weekday = px.bar(weekday, x="weekday", y="net_pnl", title="Result by Weekday")
        fig_weekday.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_weekday, use_container_width=True)

        section(t["asset_result"])
        asset = filtered_df.groupby("asset")["net_pnl"].sum().reset_index()
        fig_asset = px.bar(asset, x="asset", y="net_pnl", title="P&L by Asset")
        fig_asset.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_asset, use_container_width=True)

        section(t["risk_alerts"])
        alerts = generate_risk_alerts(filtered_df, max_daily_loss, max_drawdown_limit)
        for alert in alerts:
            st.markdown(f'<div class="alert-box">⚠️ {alert}</div>', unsafe_allow_html=True)

        if metrics["profit_factor"] < 1:
            st.error(t["pf_below_one"])

        if payoff_ratio < 1:
            st.warning(t["payoff_below_one"])

        section(t["normalized_data"])
        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            t["download_filtered"],
            csv,
            "riskpilot_filtered_trades.csv",
            "text/csv"
        )

        st.markdown(f'<div class="footer-note">{t["footer"]}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f'{t["file_error"]}: {e}')

else:
    st.info(t["send_file_to_start"])
