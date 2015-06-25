CREATE TABLE IF NOT EXISTS "app_inventory_items"
(
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES app_users(id),
    name            TEXT,
    url             TEXT,
    image_url       TEXT,
    quantity        INTEGER,
    vendor_name     TEXT,
    vendor_item_id  TEXT
);

CREATE INDEX        idx_inventory_item_name
ON                  app_inventory_items
USING               btree(name text_pattern_ops);
