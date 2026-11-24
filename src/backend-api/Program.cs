using System.Collections.Concurrent;
var app = WebApplication.CreateBuilder(args).Build();
var orders = new ConcurrentDictionary<string, Order>();
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/products/{sku}", (string sku) => sku == "DEMO-001" ? Results.Ok(new { sku, name = "Demo product" }) : Results.NotFound());
app.MapGet("/stock/{sku}", (string sku) => sku == "DEMO-001" ? Results.Ok(new { sku, stock = 42 }) : Results.NotFound());
app.MapPost("/orders", (OrderRequest request, HttpRequest http) => {
    var key = http.Headers["Idempotency-Key"].ToString();
    if (string.IsNullOrWhiteSpace(key) || key.Length > 128 || request.Sku != "DEMO-001" || request.Quantity is < 1 or > 42) return Results.BadRequest();
    var order = orders.GetOrAdd(key, _ => new Order(Guid.NewGuid(), request.Sku, request.Quantity));
    return order.Sku == request.Sku && order.Quantity == request.Quantity ? Results.Ok(order) : Results.Conflict();
});
app.Run();
record OrderRequest(string Sku, int Quantity);
record Order(Guid Id, string Sku, int Quantity);
