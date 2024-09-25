const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Create Redis client
const client = redis.createClient();

// Promisify Redis methods for async/await
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

//  Create Express instance
const app = express();
const port = 1245;

// products array
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Get an item by id
function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

// Function to reserve stock by ID in Redis
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Function to get current reserved stock by ID from Redis
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : 0;
}

// Route to get the list of all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get details of a specific product by ID, including the current stock
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.initialAvailableQuantity - currentStock;

  return res.json({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity,
    currentQuantity,
  });
});

// Route to reserve a product by ID
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  const availableStock = product.initialAvailableQuantity - currentStock;

  if (availableStock <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, currentStock + 1);
  return res.json({ status: 'Reservation confirmed', itemId });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
