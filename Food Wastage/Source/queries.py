# src/queries.py

class SQLQueries:
    
    Q_PROVIDERS = """
    SELECT 
        p."Provider_ID", 
        p."Name" AS "Provider_Name", 
        COUNT(f."Food_ID") AS "Total_Donations_Count",
        SUM(f."Quantity") AS "Total_Items_Contributed"
    FROM food_listings f
    JOIN providers p ON f."Provider_ID" = p."Provider_ID"
    GROUP BY p."Provider_ID", p."Name"
    ORDER BY "Total_Items_Contributed" DESC;
    """

    Q_HIGH_DEMAND = """
    SELECT 
        f."Location", 
        COUNT(c."Claim_ID") AS "Total_Claims",
        SUM(f."Quantity") AS "Total_Volume_Claimed"
    FROM claims c
    JOIN food_listings f ON c."Food_ID" = f."Food_ID"
    GROUP BY f."Location"
    ORDER BY "Total_Claims" DESC;
    """

    Q_WASTAGE_TRENDS = """
    SELECT 
        f."Food_Type",
        COUNT(CASE WHEN f."Expiry_Date" < CURRENT_DATE THEN 1 END) AS "Expired_Count",
        COUNT(CASE WHEN c."Status" = 'Completed' THEN 1 END) AS "Successfully_Distributed",
        ROUND(100.0 * (count(f."Food_ID")-COUNT(CASE WHEN c."Status" = 'Completed' THEN 1 END)) / COUNT(f."Food_ID"), 2) AS     "Wastage_Rate_Percentage"
    FROM food_listings f
    LEFT JOIN claims c ON f."Food_ID" = c."Food_ID"
    GROUP BY f."Food_Type";
    """
    # ============ PROVIDERS & RECEIVERS (Q1-Q4) ============
    Q1_PROVIDERS_RECEIVERS_BY_CITY = """
        SELECT p."City", COUNT(DISTINCT p."Provider_ID" ) as Total_Providers,
            (SELECT COUNT(DISTINCT r."Receiver_ID" ) FROM Receivers r WHERE r."City" = p."City") as Total_Receivers
        FROM Providers p
        GROUP BY p."City"
        ORDER BY Total_Providers DESC;
    """
    
    Q2_PROVIDER_TYPE_CONTRIBUTIONS = """
        SELECT 
            p."Type" as Provider_Type,
            COUNT(f."Food_ID") as Number_of_Listings,
            SUM(f."Quantity") as Total_Food_Quantity
        FROM Providers p
        JOIN Food_Listings f ON p."Provider_ID" = f."Provider_ID"
        GROUP BY p."Type"
        ORDER BY Total_Food_Quantity DESC;
    """
    
    Q3_PROVIDER_CONTACTS = """
        SELECT 
            "Provider_ID", "Name", "Type", "Address", "City", "Contact_Number"
        FROM Providers
        ORDER BY "City", "Name";
    """
    
    Q4_TOP_RECEIVERS = """
        SELECT 
            r."Receiver_ID", r."Name", r."Type", r."City",
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            r."Contact_Number" 
        FROM Receivers r
        JOIN Claims c ON r."Receiver_ID" = c."Receiver_ID"
        JOIN Food_Listings f ON c."Food_ID" = f."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY r."Receiver_ID", r."Name", r."Type", r."City", r."Contact_Number"
        ORDER BY Total_Quantity_Claimed DESC
        LIMIT 10;
    """
    
    # ============ FOOD LISTINGS & AVAILABILITY (Q5-Q7) ============
    
    Q5_TOTAL_FOOD_AVAILABLE = """
        SELECT 
            SUM(f."Quantity") as Total_Food_Available,
            COUNT(f."Food_ID") as Total_Food_Items,
            COUNT(DISTINCT f."Provider_ID") as Contributing_Providers
        FROM Food_Listings f
        WHERE f."Food_ID" NOT IN (SELECT "Food_ID" FROM Claims WHERE "Status" = 'Completed');
        --AND f."Expiry_Date" >= CURRENT_DATE;
    """
    
    Q6_CITY_MOST_LISTINGS = """
        SELECT 
            "Location" as City,
            COUNT("Food_ID") as Total_Food_Listings,
            SUM("Quantity") as Total_Quantity,
            COUNT(DISTINCT "Provider_ID") as Number_of_Providers
        FROM Food_Listings
        GROUP BY "Location"
        ORDER BY Total_Food_Listings DESC;
    """
    
    Q7_COMMON_FOOD_TYPES = """
        SELECT 
            "Food_Type",
            COUNT("Food_ID") as Number_of_Listings,
            SUM("Quantity") as Total_Quantity,
            ROUND(AVG("Quantity"), 2) as Average_Quantity
        FROM Food_Listings
        GROUP BY "Food_Type"
        ORDER BY Number_of_Listings DESC;
    """
    
    # ============ CLAIMS & DISTRIBUTION (Q8-Q10) ============
    
    Q8_CLAIMS_PER_FOOD = """
        SELECT 
            f."Food_ID", f."Food_Name", f."Food_Type", f."Meal_Type", f."Location",
            COUNT(c."Claim_ID") as Number_of_Claims,
            f."Quantity" as Available_Quantity
        FROM Food_Listings f
        LEFT JOIN Claims c ON f."Food_ID" = c."Food_ID"
        GROUP BY f."Food_ID", f."Food_Name", f."Food_Type", f."Meal_Type", f."Location", f."Quantity"
        ORDER BY Number_of_Claims DESC;
           
    """
    
    Q9_PROVIDER_SUCCESSFUL_CLAIMS = """
        SELECT 
            p."Provider_ID", p."Name", p."Type", p."City",
            COUNT(c."Claim_ID") as Successful_Claims,
            SUM(f."Quantity") as Total_Food_Distributed,
            p."Contact_Number"
        FROM Providers p
        JOIN Food_Listings f ON p."Provider_ID" = f."Provider_ID"
        JOIN Claims c ON f."Food_ID" = c."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY p."Provider_ID", p."Name", p."Type", p."City", p."Contact_Number"
        ORDER BY Successful_Claims DESC
        LIMIT 10;
    """
    
    Q10_CLAIM_STATUS_PERCENTAGE = """
        SELECT 
            "Status",
            COUNT("Claim_ID") as Number_of_Claims,
            ROUND(COUNT("Claim_ID") * 100.0 / (SELECT COUNT(*) FROM Claims), 2) as Percentage
        FROM Claims
        GROUP BY "Status"
        ORDER BY Number_of_Claims DESC;
    """
    
    # ============ ANALYSIS & INSIGHTS (Q11-Q13) ============
    
    Q11_AVG_QUANTITY_PER_RECEIVER = """
        SELECT 
            r."Receiver_ID", r."Name", r."Type", r."City",
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            ROUND(AVG(f."Quantity"), 2) as Average_Quantity_Per_Claim
        FROM Receivers r
        JOIN Claims c ON r."Receiver_ID" = c."Receiver_ID"
        JOIN Food_Listings f ON c."Food_ID" = f."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY r."Receiver_ID", r."Name", r."Type", r."City"
        ORDER BY Average_Quantity_Per_Claim DESC;
    """
    
    Q12_MOST_CLAIMED_MEAL_TYPE = """
        SELECT 
            f."Meal_Type",
            COUNT(c."Claim_ID") as Number_of_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            ROUND(AVG(f."Quantity"), 2) as Average_Quantity
        FROM Food_Listings f
        JOIN Claims c ON f."Food_ID" = c."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY f."Meal_Type"
        ORDER BY Number_of_Claims DESC;
    """
    
    Q13_TOTAL_DONATIONS_BY_PROVIDER = """
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
    """
    
    # ============ ADDITIONAL QUERIES (Q14-Q15) ============
    
    Q14_EXPIRING_FOOD = """
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
    """
    
    Q15_CITY_EFFICIENCY = """
        SELECT 
            f."Location" as City,
            COUNT(DISTINCT p."Provider_ID") as Total_Providers,
            COUNT(DISTINCT CASE WHEN c."Status" = 'Completed' THEN r."Receiver_ID" END) as Active_Receivers,
            COUNT(f."Food_ID") as Total_Food_Listed,
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(CASE WHEN c."Status" = 'Completed' THEN 1 ELSE 0 END) as Completed_Claims,
            SUM(CASE WHEN c."Status" = 'Pending' THEN 1 ELSE 0 END) as Pending_Claims,
            ROUND(SUM(CASE WHEN c."Status" = 'Completed' THEN 1 ELSE 0 END) * 100.0 / 
                  NULLIF(COUNT(c."Claim_ID"), 0), 2) as Success_Rate
        FROM Food_Listings f
        JOIN Providers p ON f."Provider_ID" = p."Provider_ID"
        LEFT JOIN Claims c ON f."Food_ID" = c."Food_ID"
        LEFT JOIN Receivers r ON c."Receiver_ID" = r."Receiver_ID"
        GROUP BY f."Location"
        ORDER BY Total_Claims DESC;
    """
    # ============ UTILITY METHODS ============
    @classmethod
    def get_all_queries(cls):
        """Returns dictionary of all 15 queries with user-friendly titles"""
        return {
            "🚛 Most Frequent Food Providers & Contributions": cls.Q_PROVIDERS,
            "📍 Highest Demand Locations Based on Claims": cls.Q_HIGH_DEMAND,
            "📈 Trends in Food Wastage (Expired vs Saved)": cls.Q_WASTAGE_TRENDS,
            "📍 Food Distribution Insights by City": cls.Q1_PROVIDERS_RECEIVERS_BY_CITY,
            "📊 Donation Contribution by Provider Type": cls.Q2_PROVIDER_TYPE_CONTRIBUTIONS,
            "📞 Active Provider Contact Directory": cls.Q3_PROVIDER_CONTACTS,
            "🏆 Top Food Receivers & Claim Counts": cls.Q4_TOP_RECEIVERS,
            "🍏 Current Available & Unexpired Food": cls.Q5_TOTAL_FOOD_AVAILABLE,
            "🏢 Cities with Highest Donation Volume": cls.Q6_CITY_MOST_LISTINGS,
            "🍲 Most Frequently Donated Food Categories": cls.Q7_COMMON_FOOD_TYPES,
            "📋 Demand Tracker: Claims per Food Item": cls.Q8_CLAIMS_PER_FOOD,
            "✅ Most Successful Food Providers": cls.Q9_PROVIDER_SUCCESSFUL_CLAIMS,
            "📈 Overall Claim Status Breakdown": cls.Q10_CLAIM_STATUS_PERCENTAGE,
            "⚖️ Average Quantity Distributed per Receiver": cls.Q11_AVG_QUANTITY_PER_RECEIVER,
            "🍕 Most Popular Meal Types Requested": cls.Q12_MOST_CLAIMED_MEAL_TYPE,
            "💰 Total Historical Donations per Provider": cls.Q13_TOTAL_DONATIONS_BY_PROVIDER,
            "⚠️ Critical: Food Expiring within 3 Days": cls.Q14_EXPIRING_FOOD,
            "⚡ Operational Efficiency Metrics by City": cls.Q15_CITY_EFFICIENCY
        }

    @classmethod
    def get_query_by_number(cls, num):
        """Get query by number (1-18)"""
        queries = [
            cls.Q_PROVIDERS,cls.Q_HIGH_DEMAND,cls.Q_WASTAGE_TRENDS,
            cls.Q1_PROVIDERS_RECEIVERS_BY_CITY, cls.Q2_PROVIDER_TYPE_CONTRIBUTIONS,
            cls.Q3_PROVIDER_CONTACTS, cls.Q4_TOP_RECEIVERS,
            cls.Q5_TOTAL_FOOD_AVAILABLE, cls.Q6_CITY_MOST_LISTINGS,
            cls.Q7_COMMON_FOOD_TYPES, cls.Q8_CLAIMS_PER_FOOD,
            cls.Q9_PROVIDER_SUCCESSFUL_CLAIMS, cls.Q10_CLAIM_STATUS_PERCENTAGE,
            cls.Q11_AVG_QUANTITY_PER_RECEIVER, cls.Q12_MOST_CLAIMED_MEAL_TYPE,
            cls.Q13_TOTAL_DONATIONS_BY_PROVIDER, cls.Q14_EXPIRING_FOOD,
            cls.Q15_CITY_EFFICIENCY
        ]
        return queries[num - 1] if 1 <= num <= 18 else None
    
    
