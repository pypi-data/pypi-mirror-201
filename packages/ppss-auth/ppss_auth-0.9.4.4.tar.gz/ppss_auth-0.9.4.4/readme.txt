** To create a new ppss_auth db revision:
cd ppss_auth/alembic
alembic -c alembic.ini revision --autogenerate -m "your comment here"
** then execute it with
alembic -c alembic.ini upgrade HEAD

** babel/i18n
requires
apt install gettext
pip install babel

#extract strings from py, jinja2, mako
pybabel extract -F babel.ini -o ${project}/locale/${project}.pot ${project} 
#pybabel extract -F babel.ini -k _t:2 -o ${project}/locale/${project}.pot ${project} 

#first time creation
mkdir -p ${project}/${lang}/LC_MESSAGES
msginit -l ${lang} -o ${project}/locale/${lang}/LC_MESSAGES/${project}.po --input ${project}/locale/${project}.pot

#update
msgmerge --update ${project}/locale/${lang}/LC_MESSAGES/${project}.po ${project}/locale/${project}.pot

#compile .po into .mo
msgfmt -o ${project}/locale/${lang}/LC_MESSAGES/${project}.mo ${project}/locale/${lang}/LC_MESSAGES/${project}.po



##useful view for manual queries:
create view ppssauth_user_view as
select distinct u.id as user_id,u.username as user_name ,u.enabled as enabled,p.name as permission from ums.ppss_permission as p
inner join ppssgroup_lk_ppsspermission as glkp on glkp.permission_id = p.id
inner join ppss_group as g on glkp.group_id = g.id
inner join ppssuser_lk_ppssgroup as ulkg on ulkg.group_id = glkp.group_id
inner join ppss_user as u on u.id = ulkg.user_id
where g.enabled = 1;