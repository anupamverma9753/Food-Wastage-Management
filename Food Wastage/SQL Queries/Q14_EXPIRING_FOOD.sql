
        SELECT 
            f."Food_ID", f."Food_Name", f."Quantity", f."Expiry_Date",
            (f."Expiry_Date" - CURRENT_DATE) as Days_Until_Expiry,
            p."Name" as Provider_Name, p."Contact_Number" as Provider_Contact,
            f."Location", f."Food_Type", f."Meal_Type"
        FROM Food_Listings f
        JOIN Providers p ON f."Provider_ID" = p."Provider_ID"
        WHERE f."Expiry_Date" >= CURRENT_DATE
          AND f."Expiry_Date" <= CURRENT_DATE + INTERVAL '3 days'
          AND f."Food_ID" NOT IN (SELECT "Food_ID" FROM Claims WHERE "Status" = 'Completed')
        ORDER BY f."Expiry_Date" ASC;