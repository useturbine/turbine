// Switch to the desired database
db = db.getSiblingDB("test");

// Create a collection named "products"
db.createCollection("users");

// Insert sample data into the "products" collection
db.users.insertMany([
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob", email: "bob@example.com" },
  // ... more sample data
]);

print("Sample data has been inserted into the 'products' collection.");
