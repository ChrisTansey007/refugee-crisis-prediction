-- Database initialization script
-- This script runs on first container start

CREATE EXTENSION IF NOT EXISTS postgis;

-- Create regions table if it doesn't exist
CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Preload sample admin regions (subset for demo)
-- In production, load full GADM or similar dataset
INSERT INTO regions (name, code) VALUES
('Afghanistan', 'AFG'),
('Syria', 'SYR'),
('Iraq', 'IRQ'),
('Yemen', 'YEM'),
('South Sudan', 'SSD'),
('Somalia', 'SOM'),
('Democratic Republic of the Congo', 'COD'),
('Ethiopia', 'ETH'),
('Sudan', 'SDN')
ON CONFLICT (code) DO NOTHING;

-- TODO: Add geometry data from GADM shapefiles in Phase 2