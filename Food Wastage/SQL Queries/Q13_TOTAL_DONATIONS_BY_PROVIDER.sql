
        SELECT 
            p."Provider_ID", p."Name", p."Type", p."City",
            COUNT(f."Food_ID") as Number_of_Donations,
            SUM(f."Quantity") as Total_Quantity_Donated,
            ROUND(AVG(f."Quantity"), 2) as Average_Donation_Size,
            p."Contact_Number"
        FROM Providers p
        JOIN Food_Listings f ON p."Provider_ID"= f."Provider_ID"
        GROUP BY p."Provider_ID", p."Name", p."Type", p."City", p."Contact_Number" 
        ORDER BY Total_Quantity_Donated DESC;