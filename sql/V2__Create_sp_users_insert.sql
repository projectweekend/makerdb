CREATE FUNCTION sp_users_insert
(
    userDoc JSON
)

RETURNS TABLE
(
    resultDoc JSON
) AS

$$
BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_users
                        (
                            email,
                            password
                        )
        VALUES          (
                            CAST(userDoc ->> 'email' AS VARCHAR),
                            CAST(userDoc ->> 'password' AS VARCHAR)
                        )
        RETURNING       app_users.id,
                        app_users.email,
                        app_users.is_active,
                        app_users.is_admin
    )
    SELECT      ROW_TO_JSON(i.*)
    FROM        i;
END;
$$

LANGUAGE plpgsql;
