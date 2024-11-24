INSERT INTO post (id, body, created_at, updated_at, deleted_at)
VALUES
  (1, 'test' || x'0a' || 'body', '2018-01-01 00:00:00', NULL, NULL),
  (2, 'test deleted', '2018-01-01 00:00:00', NULL, '2018-02-01 00:00:00');

INSERT INTO message (content, created_at)
VALUES
  ('happy content1', '2018-01-01 00:00:00'),
  ('happy content2', '2018-01-02 00:00:00');
