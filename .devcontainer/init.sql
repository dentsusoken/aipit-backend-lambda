DROP TABLE IF EXISTS "SampleTable";
DROP TABLE IF EXISTS "SignatureTable";

CREATE TABLE "SampleTable" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE "SignatureTable" (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_data VARCHAR(1024),
    signed_data VARCHAR(2048)
);