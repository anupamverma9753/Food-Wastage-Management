 
        SELECT p."City", COUNT(DISTINCT p."Provider_ID" ) as Total_Providers,
            (SELECT COUNT(DISTINCT r."Receiver_ID" ) FROM Receivers r WHERE r."City" = p."City") as Total_Receivers
        FROM Providers p
        GROUP BY p."City"
        ORDER BY Total_Providers DESC;