CREATE TABLE filmes (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    titulo VARCHAR(255),
    categoria VARCHAR(50),
    diretor VARCHAR(50),
    sinopse TEXT,
    ano INT,
    duracao INT
);

INSERT INTO filmes (titulo, diretor, categoria, sinopse, duracao, ano) VALUES 
    ('pulp fiction', 'tarantino', 'cult', 'nao sei', 120, 1994),
    ('the shining', 'kubrick', 'cult', 'nao sei', 120, 1989),
    ('drive', ' Nicolas Winding ', 'acao', 'nao sei', 120, 2012);


ALTER TABLE filmes DROP diretor;
ALTER TABLE filmes MODIFY categoria VARCHAR(100);


SELECT categoria, COUNT(*) FROM filmes /*query group by*/
GROUP BY categoria;

SELECT titulo FROM filmes /*query order by*/
ORDER BY ano;


SELECT categoria FROM filmes  /*query com comparação lógica*/
WHERE ano = 1994;
