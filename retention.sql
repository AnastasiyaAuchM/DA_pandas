-- Decision for building a pivot table in Redash:
--     https://drive.google.com/file/d/17wdhtXNGlZ_CSM228NfgnR7avjNxrKMT/view?usp=sharing
-- Scheme db: 
--     https://drive.google.com/file/d/1K6Sj5NgmwEGXX-XmiycA_Pdul5lJsOQc/view?usp=sharing 


SELECT
  date_trunc('month', start_date) :: date AS start_month,
  start_date,
  active_dt - start_date AS day_number,
  ROUND(count(DISTINCT user_id) :: decimal / MAX(count(DISTINCT user_id)) 
         OVER (PARTITION BY start_date), 2) AS retention
FROM
  (
    SELECT
      user_id,
      min(time :: date) OVER (PARTITION BY user_id) as start_date,
      time :: date AS active_dt
    FROM user_actions
  ) t1
GROUP BY
  active_dt, start_date
ORDER BY
  start_date, day_number
