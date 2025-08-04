-- hlavni tabulka veci
CREATE TABLE veci (
    id SERIAL PRIMARY KEY,
    co_to_je TEXT,
    porcelan BOOLEAN,
    cena TEXT,
    kde_je TEXT,
    krabice TEXT,
    pokoj TEXT,
    description TEXT,
    poznamka TEXT,
    prodat TEXT,
    tags TEXT,
    file_path TEXT,
    url TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- data do veci
INSERT INTO veci (co_to_je, porcelan, cena, kde_je, krabice, pokoj, description, poznamka, prodat, tags, file_path, url)
VALUES
('Modrý hrnek', TRUE, 250, 'Kuchyň', 'Ano', 'Pokoj 1', 'Krásný starožitný hrnek', 'Bez poškození', 'Ne', 'porcelan,hrnek', '/cesta/k/fotce/hrnek.jpg', 'https://example.com/hrnek');



-- tabulka porcelan
CREATE TABLE porcelan_info (
    id SERIAL PRIMARY KEY,
    vec_id INTEGER REFERENCES veci(id) ON DELETE CASCADE,
    znacka TEXT,
    puvod TEXT,
    rozmer TEXT,
    stav TEXT,
    zajimavost TEXT,
    foto_vady TEXT[], -- pole s cestami k fotkám vad
    date_added TIMESTAMP DEFAULT NOW()
);

-- data do porcelan info
INSERT INTO porcelan_info (vec_id, znacka, puvod, rozmer, stav, zajimavost, foto_vady)
VALUES
(1, 'Thun', 'Česká republika', '10x10x10 cm', 'Výborný', 'Limitovaná edice 1920', ARRAY['/cesta/k/fotce/vada1.jpg', '/cesta/k/fotce/vada2.jpg']);


