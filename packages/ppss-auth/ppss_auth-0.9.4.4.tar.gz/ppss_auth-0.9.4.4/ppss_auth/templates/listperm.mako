<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>${_('Name', domain='ppss_auth')}</th>
			<th>${_('System', domain='ppss_auth')}</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${_("Yes", domain='ppss_auth') if e.permtype == 1 else _("No", domain='ppss_auth')}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid=e.id)}">${_('delete', domain='ppss_auth')}</a><br/>
					<!--a href="${request.route_url('ppss:user:changepassword',userid=e.id)}">modify</a><br/-->

				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid = -1)}">${_('Add Perm', domain='ppss_auth')}</a>
</div>