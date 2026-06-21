
        SELECT 
            p."Type" as Provider_Type,
            COUNT(f."Food_ID") as Number_of_Listings,
            SUM(f."Quantity") as Total_Food_Quantity
        FROM Providers p
        JOIN Food_Listings f ON p."Provider_ID" = f."Provider_ID"
        GROUP BY p."Type"
        ORDER BY Total_Food_Quantity DESC;