-- 2) Préparer des vues “Gold” pour la démo (TOP N, tendance, forecast) Northwind a des dates fin 1996–1998. On se base sur ShippedDate (plus complète) ; si NULL, on retombe sur OrderDate.
-- 2.1 Vue des lignes de vente (détails étendus)
CREATE OR ALTER VIEW dbo.vw_SalesLines AS
SELECT 
    od.OrderID,
    o.CustomerID,
    o.EmployeeID,
    COALESCE(o.ShippedDate, o.OrderDate) AS SalesDate,
    od.ProductID,
    p.ProductName,
    od.UnitPrice,
    od.Quantity,
    od.Discount,
    CAST(od.UnitPrice * od.Quantity * (1 - od.Discount) AS money) AS LineAmount
FROM [Order Details] od
JOIN Orders o        ON o.OrderID = od.OrderID
JOIN Products p      ON p.ProductID = od.ProductID;

-- 2.2 Vue ventes hebdo par produit (alimentera le modèle)
CREATE OR ALTER VIEW dbo.vw_WeeklySalesByProduct AS
SELECT
    ProductID,
    ProductName,
    DATEADD(WEEK, DATEDIFF(WEEK, 0, SalesDate), 0) AS WeekStart,
    SUM(LineAmount) AS SalesAmount
FROM dbo.vw_SalesLines
GROUP BY
    ProductID, ProductName,
    DATEADD(WEEK, DATEDIFF(WEEK, 0, SalesDate), 0);

-- 2.3 Vue top produits rolling 8 semaines (pour l’agent SQL)
CREATE OR ALTER VIEW dbo.vw_TopProducts_8w AS
WITH base AS (
  SELECT *, DATEADD(WEEK, DATEDIFF(WEEK, 0, GETDATE()), 0) AS ThisWeek
  FROM dbo.vw_WeeklySalesByProduct
)
SELECT TOP 10
  ProductID, ProductName,
  SUM(SalesAmount) AS SalesAmount_8w
FROM base
WHERE WeekStart >= DATEADD(WEEK, -8, ThisWeek)
GROUP BY ProductID, ProductName
ORDER BY SalesAmount_8w DESC;

-- (Si tu veux “figer” une période cohérente avec 1997, remplace GETDATE() par '1998-03-01' par ex.)
