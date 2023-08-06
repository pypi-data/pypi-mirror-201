-- Auto generated test script file from rdbunit
-- Input from chat.rdbu
ATTACH DATABASE ":memory:" AS test_default;

-- BEGIN SETUP
DROP TABLE IF EXISTS relationships;
CREATE TABLE relationships(id INTEGER, parent_id INTEGER);
INSERT INTO relationships VALUES (1, 2);
INSERT INTO relationships VALUES (2, 3);
INSERT INTO relationships VALUES (3, NULL);

-- BEGIN SELECT
CREATE VIEW test_select_result AS
WITH RECURSIVE cte AS (
  SELECT id, parent_id
  FROM relationships
  WHERE parent_id IS NULL
  UNION ALL
  SELECT relationships.id, relationships.parent_id
  FROM relationships
  INNER JOIN cte ON relationships.parent_id = cte.id
)
SELECT id, parent_id
FROM cte;

-- BEGIN RESULT
DROP TABLE IF EXISTS test_expected;
CREATE TABLE test_expected(id INTEGER, parent_id INTEGER);
INSERT INTO test_expected VALUES (1, 3);
INSERT INTO test_expected VALUES (2, 3);
INSERT INTO test_expected VALUES (3, NULL);

        SELECT CASE WHEN
          (SELECT COUNT(*) FROM (
            SELECT * FROM test_expected
            UNION
            SELECT * FROM test_select_result
          ) AS u1) = (SELECT COUNT(*) FROM test_expected) AND
          (SELECT COUNT(*) FROM (
            SELECT * FROM test_expected
            UNION
            SELECT * FROM test_select_result
          ) AS u2) = (SELECT COUNT(*) FROM test_select_result)
THEN 'ok 1 - chat.rdbu: test_select_result' ELSE
'not ok 1 - chat.rdbu: test_select_result' END;

SELECT '1..1';
