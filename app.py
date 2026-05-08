import streamlit as st
            st.markdown(f'<div class="insight-box"><div class="metric-label">Pior horário</div><div class="metric-value negative">{worst_hour}h</div><div class="metric-help">Resultado: {money(worst_hour_pnl)}</div></div>', unsafe_allow_html=True)
        with i3:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Melhor dia</div><div class="metric-value positive">{best_day}</div><div class="metric-help">Resultado: {money(best_day_pnl)}</div></div>', unsafe_allow_html=True)
        with i4:
            st.markdown(f'<div class="insight-box"><div class="metric-label">Pior dia</div><div class="metric-value negative">{worst_day}</div><div class="metric-help">Resultado: {money(worst_day_pnl)}</div></div>', unsafe_allow_html=True)

        section("6. Painel Prop Firm")

        remaining_target = profit_target - metrics["net_pnl"]
        daily_worst = filtered_df.groupby("day")["net_pnl"].sum().min()
        daily_remaining = max_daily_loss - abs(daily_worst)
        max_dd_remaining = max_drawdown_limit - abs(metrics["max_drawdown"])

        prop1, prop2, prop3 = st.columns(3)
        with prop1:
            st.markdown(f'<div class="prop-card"><div class="metric-label">🎯 Distância da Meta</div><div class="metric-value neutral">{money(remaining_target)}</div><div class="metric-help">Faltam para atingir o objetivo configurado</div></div>', unsafe_allow_html=True)
        with prop2:
            st.markdown(f'<div class="prop-card"><div class="metric-label">⚠️ Daily DD Restante</div><div class="metric-value {"negative" if daily_remaining < 0 else "neutral"}">{money(daily_remaining)}</div><div class="metric-help">Margem restante até o limite diário</div></div>', unsafe_allow_html=True)
        with prop3:
            st.markdown(f'<div class="prop-card"><div class="metric-label">🛑 Max DD Restante</div><div class="metric-value {"negative" if max_dd_remaining < 0 else "neutral"}">{money(max_dd_remaining)}</div><div class="metric-help">Margem restante até o drawdown máximo</div></div>', unsafe_allow_html=True)

        section("7. Curva de Capital")
        fig_equity = px.line(filtered_df, x="date", y="equity", title="Equity Curve")
        fig_equity.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_equity, use_container_width=True)

        section("8. Drawdown")
        fig_dd = px.area(filtered_df, x="date", y="drawdown", title="Drawdown")
        fig_dd.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_dd, use_container_width=True)

        section("9. Resultado por Dia")
        daily_pnl = filtered_df.groupby("day")["net_pnl"].sum().reset_index()
        fig_daily = px.bar(daily_pnl, x="day", y="net_pnl", title="Daily P&L")
        fig_daily.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_daily, use_container_width=True)

        section("10. Resultado por Hora")
        hourly = filtered_df.groupby("hour")["net_pnl"].sum().reset_index()
        fig_hour = px.bar(hourly, x="hour", y="net_pnl", title="Resultado por Hora")
        fig_hour.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_hour, use_container_width=True)

        section("11. Resultado por Dia da Semana")
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = filtered_df.groupby("weekday")["net_pnl"].sum().reset_index()
        weekday["weekday"] = pd.Categorical(weekday["weekday"], categories=weekday_order, ordered=True)
        weekday = weekday.sort_values("weekday")
        fig_weekday = px.bar(weekday, x="weekday", y="net_pnl", title="Resultado por Dia da Semana")
        fig_weekday.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_weekday, use_container_width=True)

        section("12. Resultado por Ativo")
        asset = filtered_df.groupby("asset")["net_pnl"].sum().reset_index()
        fig_asset = px.bar(asset, x="asset", y="net_pnl", title="P&L por Ativo")
        fig_asset.update_layout(template="plotly_dark", height=430)
        st.plotly_chart(fig_asset, use_container_width=True)

        section("13. Alertas de Risco")
        alerts = generate_risk_alerts(filtered_df, max_daily_loss, max_drawdown_limit)
        for alert in alerts:
            st.markdown(f'<div class="alert-box">⚠️ {alert}</div>', unsafe_allow_html=True)

        if metrics["profit_factor"] < 1:
            st.error("Profit Factor abaixo de 1. Você está perdendo mais do que ganha.")

        if payoff_ratio < 1:
            st.warning("Seu payoff está abaixo de 1. Seus losses estão maiores que seus gains.")

        section("14. Dados Normalizados")
        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Baixar dados filtrados normalizados",
            csv,
            "riskpilot_filtered_trades.csv",
            "text/csv"
        )

        st.markdown('<div class="footer-note">RiskPilot MVP — Trading risk analytics for serious traders.</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

else:
    st.info("Envie um arquivo CSV ou XLSX para começar.")
