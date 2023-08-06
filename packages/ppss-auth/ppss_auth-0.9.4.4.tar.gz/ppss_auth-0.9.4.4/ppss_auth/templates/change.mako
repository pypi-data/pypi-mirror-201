<%inherit file="${context['logintpl']}" />
<div class="container">
  <div class="row text-center">
      <div class="${bc['xs']}12 col-md-4 offset-md-4">
        <form action="${request.route_url('ppss:user:changepassword')}" method="POST" class="ppssauthform">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
            <h2>${_("Change password for user {username}", domain='ppss_auth').format(username=request.loggeduser.username) }</h2>
            <input type="password" name="oldpassword" autocomplete="off" placeholder="${_('current password', domain='ppss_auth')}">
            <br/>
            <input type="password" name="newpassword" autocomplete="off" placeholder="${_('new password', domain='ppss_auth')}">
            <br/>
            <input type="password" name="confirmnewpassword" autocomplete="off" placeholder="${_('confirm new password', domain='ppss_auth')}">
            <br/>
            <div class="text-center">
              <input type="submit" name="submit" value="${_('update', domain='ppss_auth')}"/>
            </div>

            <p>${msg}</p>
        </form>
      </div>
  </div>
</div>
