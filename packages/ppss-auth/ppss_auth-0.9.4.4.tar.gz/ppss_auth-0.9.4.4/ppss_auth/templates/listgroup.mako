<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>${_('Group name', domain='ppss_auth')}</th>
			<th>${_('Permissions', domain='ppss_auth')}</th>
			<th>${_('Enabled', domain='ppss_auth')}</th>
			
			<th>${_('Action', domain='ppss_auth')}</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${", ".join([p.name for p in e.permissions])}</td>
				<td>${_("Yes", domain='ppss_auth') if e.enabled else _("No", domain='ppss_auth')}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid=e.id)}">${_('modify', domain='ppss_auth')}</a><br/>
				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid = -1)}">${_('Add Group', domain='ppss_auth')}</a>
</div>