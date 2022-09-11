
-- @author: "Arnoldo J. González Quesada".
-- Github username: "ArnoldG6".
-- Contact me via "arnoldgq612@gmail.com".
-- GPL-3.0 license ©2022
-- =============================================t_user data==============================================
insert into t_user
(id,
  username,
  email,
  pwd_hash,
  creation_datetime,
  first_name,
  last_name,
  token,
  enabled
) VALUES (
1,
'arnold',
'arnoldgq612@gmail.com',
'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
NOW(),
'Arnold',
'González',
NULL,true
);
-- =============================================t_role data==============================================
insert into t_role (id,name,description,creation_datetime)
VALUES (1,'CLIENT','Can access to common-user functions in the website.', NOW());
-- =========================================t_permission data============================================
insert into t_permission (id,name,creation_datetime,description)
VALUES (1,'SET_ACCOUNT_BALANCE', NOW(),'User can add or withdraw money-representation from account.');
-- =======================================t_user_role data===============================================
insert into t_user_role (user_id, role_id) VALUES (1,1);
-- =====================================t_role_permission data===========================================
insert into t_role_permission(role_id, permission_id) VALUES(1,1);
