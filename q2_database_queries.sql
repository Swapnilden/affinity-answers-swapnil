-- QUESTION 2a: Count Acacia plants
SELECT COUNT(*) 
FROM taxonomy 
WHERE species LIKE '%Acacia%';

-- QUESTION 2b: Wheat with longest DNA
SELECT t.species, MAX(r.length) as max_sequence_length
FROM taxonomy t
JOIN rfamseq r ON t.ncbi_id = r.ncbi_id
WHERE t.species LIKE '%Triticum%' OR t.tax_string LIKE '%Wheat%'
GROUP BY t.species
ORDER BY max_sequence_length DESC
LIMIT 1;

-- QUESTION 2c: Pagination query
SELECT f.rfam_acc, f.rfam_id, MAX(r.length) as max_dna_length
FROM family f
JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN rfamseq r ON fr.rfamseq_acc = r.rfamseq_acc
GROUP BY f.rfam_acc, f.rfam_id
HAVING max_dna_length > 1000000
ORDER BY max_dna_length DESC
LIMIT 15 OFFSET 120;
