SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A'
AND teacher_id = (
    SELECT teacher_id
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
