BEGIN TRANSACTION;

INSERT INTO attributes (name, area, custom) VALUES
  ('clarity', 'mind', FALSE),
  ('memory', 'mind', FALSE),
  ('thinking', 'mind', FALSE),
  ('imagination', 'mind', FALSE),
  ('acceptance', 'spirit', FALSE),
  ('activeness', 'spirit', FALSE),
  ('bravery', 'spirit', FALSE),
  ('trust', 'spirit', FALSE),
  ('positivity', 'spirit', FALSE),
  ('strength', 'body', FALSE),
  ('flexibility', 'body', FALSE),
  ('speed', 'body', FALSE),
  ('appearance', 'body', FALSE);

COMMIT;