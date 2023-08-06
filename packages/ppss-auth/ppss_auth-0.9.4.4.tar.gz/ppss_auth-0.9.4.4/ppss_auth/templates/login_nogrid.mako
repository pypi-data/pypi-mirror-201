<%inherit file="${context['logintpl']}" />
<form action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
    % if request.loggeduser: 
    <p>
        ${_('You are already logged in as', domain='ppss_auth')} <a href="${request.route_url('ppss:user:editself')}">${request.loggeduser.username}</a>. <a href="${request.route_url('ppsslogout')}">Logout</a>?<br/>
        ${signinreason}<br/>
        ${_("You can proceed to your main page following this ") }<a href="${request.route_url(request.ppssauthconf.postloginroute)}">${_("link")}</a>.<br/>
    </p>
    % endif
    <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
    <input class="form-control" type="text" name="${_('username', domain='ppss_auth')}" placeholder="username">
    <br/>
    <input class="form-control" type="password" autocomplete="off" name="${_('password', domain='ppss_auth')}" placeholder="password">
    <br/>
    <div class="text-center">
        <input class="btn btn-success" type="submit" name="submit" value="${_('Login', domain='ppss_auth')}"/>
    </div>
    </br>
    <p class="text-danger">${msg}</p>
</form>