
        SELECT 
            "Status",
            COUNT("Claim_ID") as Number_of_Claims,
            ROUND(COUNT("Claim_ID") * 100.0 / (SELECT COUNT(*) FROM Claims), 2) as Percentage
        FROM Claims
        GROUP BY "Status"
        ORDER BY Number_of_Claims DESC;