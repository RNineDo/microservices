$BASE = "http://localhost:8000/api"
$ErrorActionPreference = "Continue"

function Test-Route {
    param($Method, $Uri, $Body, $Label)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "TEST: $Label" -ForegroundColor Cyan
    Write-Host "$Method $Uri" -ForegroundColor Yellow
    try {
        if ($Body) {
            $json = $Body | ConvertTo-Json -Depth 5
            Write-Host "Body: $json" -ForegroundColor DarkGray
            $resp = Invoke-RestMethod -Uri $Uri -Method $Method -Body $json -ContentType "application/json"
        } else {
            $resp = Invoke-RestMethod -Uri $Uri -Method $Method -ContentType "application/json"
        }
        $result = $resp | ConvertTo-Json -Depth 5
        Write-Host "REPONSE OK:" -ForegroundColor Green
        Write-Host $result
        return $resp
    } catch {
        Write-Host "ERREUR: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host "============================================" -ForegroundColor Magenta
Write-Host "   TESTS API MICROSERVICES (pyzmq)" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "Attente du demarrage des services (10s)..."
Start-Sleep -Seconds 10

$warehouse = Test-Route -Method "POST" -Uri "$BASE/warehouse" -Label "Creer un entrepot" -Body @{
    name = "Entrepot Lyon"
    address = "45 rue de la Republique, Lyon"
}
$warehouseId = $warehouse.id

$product = Test-Route -Method "POST" -Uri "$BASE/product" -Label "Creer un produit" -Body @{
    name = "Clavier mecanique RGB"
    description = "Clavier gaming switches rouges"
    category = "electronics"
}
$productId = $product.id

Write-Host "`nAttente propagation evenements SUB (3s)..." -ForegroundColor DarkYellow
Start-Sleep -Seconds 3

$productDetail = Test-Route -Method "GET" -Uri "$BASE/product/$productId" -Label "Recuperer produit (PAIR pricing + PAIR inventory)"

$customer = Test-Route -Method "POST" -Uri "$BASE/customer" -Label "Creer un client (PUB customer.created)" -Body @{
    first_name = "Jean"
    last_name = "Dupont"
    email = "jean.dupont@mail.fr"
    phone = "0612345678"
}
$customerId = $customer.id

Test-Route -Method "GET" -Uri "$BASE/customer/$customerId" -Label "Recuperer le client"
Test-Route -Method "GET" -Uri "$BASE/warehouse" -Label "Lister les entrepots"
Test-Route -Method "GET" -Uri "$BASE/pricing/$productId" -Label "Verifier pricing auto-cree (SUB product.created -> pricing)"
Test-Route -Method "GET" -Uri "$BASE/inventory/$productId" -Label "Verifier inventaire auto-cree (SUB product.created -> inventory)"

Test-Route -Method "PATCH" -Uri "$BASE/inventory/$warehouseId/$productId" -Label "Modifier le stock a 50" -Body @{
    quantity = 50
}

Test-Route -Method "PUT" -Uri "$BASE/product/$productId" -Label "Modifier le produit" -Body @{
    name = "Clavier mecanique RGB Pro"
}

$order = Test-Route -Method "POST" -Uri "$BASE/order" -Label "Creer commande (PUB orderline.created)" -Body @{
    customer_id = $customerId
    lines = @(
        @{
            product_id = $productId
            quantity = 3
            warehouse_id = $warehouseId
        }
    )
}
$orderId = $order.id

Write-Host "`nAttente propagation evenements SUB (3s)..." -ForegroundColor DarkYellow
Start-Sleep -Seconds 3

Test-Route -Method "GET" -Uri "$BASE/order/$orderId" -Label "Recuperer la commande"
Test-Route -Method "PATCH" -Uri "$BASE/order/$orderId" -Label "Passer en confirmed" -Body @{ status = "confirmed" }
Test-Route -Method "GET" -Uri "$BASE/inventory/$productId" -Label "Verifier stock decremente (SUB orderline.created -> inventory)"

Write-Host "`n============================================" -ForegroundColor Magenta
Write-Host "   RESUME" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta
Write-Host "Patterns ZeroMQ testes:" -ForegroundColor Green
Write-Host "  [REQ/REP] Gateway <-> tous les services" -ForegroundColor Green
Write-Host "  [PUB/SUB] product.created -> pricing + inventory" -ForegroundColor Green
Write-Host "  [PUB/SUB] customer.created" -ForegroundColor Green
Write-Host "  [PUB/SUB] orderline.created -> inventory (decremente stock)" -ForegroundColor Green
Write-Host "  [PAIR]    product <-> pricing (get_price)" -ForegroundColor Green
Write-Host "  [PAIR]    product <-> inventory (get_stock)" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Magenta
