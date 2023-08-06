<div class="ppss_auth--usermanage">
  % if 'user' in request.session:
    ${_('Hi', domain='ppss_auth')} <strong>${request.session['user']['name']}</strong><br>
    <small>${_('Not', domain='ppss_auth')} ${request.session['user']['name']}? <a href="${request.route_url('ppsslogout')}">Logout</a>
  % else:
    <a href="${request.route_url('ppsslogin')}">${_('Login', domain='ppss_auth')}</a>
  % endif
</div>