BEGIN TRANSACTION;

INSERT INTO base_activities (name, xp, activity_type) VALUES
  ('create', 100, 'base'),
  ('search', 100, 'base'),
  ('order', 100, 'base'),
  ('deduce', 100, 'base'),
  ('learn', 100, 'base'),
  ('experiance', 100, 'base'),
  ('other', 100, 'base');

COMMIT;