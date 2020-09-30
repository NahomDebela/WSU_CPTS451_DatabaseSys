UPDATE Business AS Btbl
SET numcheckins = Ctbl.total_checkins
FROM
(
	SELECT Checkin.business_id, COUNT(Checkin.business_id) AS total_checkins
	FROM Checkin
	GROUP BY Checkin.business_id
) AS Ctbl
WHERE Ctbl.business_id = Btbl.business_id

UPDATE Business AS Btbl
SET numtips = Ttbl.total_tips
FROM
(
	SELECT Tip.business_id, COUNT(Tip.business_id) AS total_tips
	FROM Tip
	GROUP BY Tip.business_id 
) AS Ttbl
WHERE Ttbl.business_id = Btbl.business_id

UPDATE Users AS Utbl
SET totalLikes = Ttbl.total_likes
FROM
(
	SELECT Tip.user_id, SUM(Tip.likes) AS total_likes
	FROM Tip
	GROUP BY Tip.user_id
) AS Ttbl
WHERE Ttbl.user_id = Utbl.user_id

UPDATE Users AS Utbl
SET tip_count = Ttbl.total_tips
FROM
(
	SELECT Tip.user_id, COUNT(Tip.user_id) AS total_tips
	FROM Tip
	GROUP BY Tip.user_id
) AS Ttbl
WHERE Ttbl.user_id = Utbl.user_id


