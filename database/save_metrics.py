from sqlalchemy import text

from database.postgres_sql import get_engine


def save_metrics(
    company: str,
    year: int,
    metrics: dict
) -> None:
    engine = get_engine()

    query = """
    INSERT INTO financial_metrics (
        company, year, revenue, net_income, operating_income,
        cash_flow, total_assets, total_liabilities, risk_factors, growth_drivers
    )
    VALUES (
        :company, :year, :revenue, :net_income, :operating_income,
        :cash_flow, :total_assets, :total_liabilities, :risk_factors, :growth_drivers
    )
    """

    params = {
        "company": company,
        "year": str(year),
        "revenue": metrics.get("Revenue") or metrics.get("revenue"),
        "net_income": metrics.get("Net Income") or metrics.get("net_income"),
        "operating_income": metrics.get("Operating Income") or metrics.get("operating_income"),
        "cash_flow": metrics.get("Cash Flow from Operating Activities") or metrics.get("cash_flow"),
        "total_assets": metrics.get("Total Assets") or metrics.get("total_assets"),
        "total_liabilities": metrics.get("Total Liabilities") or metrics.get("total_liabilities"),
        "risk_factors": "\n".join(metrics.get("Top Risk Factors", []) or metrics.get("risk_factors", [])),
        "growth_drivers": "\n".join(metrics.get("Top Growth Drivers", []) or metrics.get("growth_drivers", []))
    }

    with engine.begin() as connection:
        connection.execute(text(query), params)

    print(f"Successfully saved metrics for {company} {year}")
