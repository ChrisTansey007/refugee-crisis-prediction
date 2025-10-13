-- Database initialization script
-- This script runs on first container start

CREATE EXTENSION IF NOT EXISTS postgis;

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
('Sudan', 'SDN');

-- TODO: Add geometry data from GADM shapefiles in Phase 2
