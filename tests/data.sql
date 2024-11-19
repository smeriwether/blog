INSERT INTO post (body, created)
VALUES
  ('test' || x'0a' || 'body', '2018-01-01 00:00:00');

INSERT INTO message (content, created)
VALUES
  ('happy content1', '2018-01-01 00:00:00'),
  ('happy content2', '2018-01-02 00:00:00');
