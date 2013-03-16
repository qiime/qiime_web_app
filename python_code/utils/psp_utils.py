def format_submit_form_to_fusebox_string(**kwargs):
    """Get string for javasript-based redirect

    creates hidden form elements for each argument, and then submits that
    form to fusebox.

    if form_name is in **kwargs, the form will be given that name and id
    otherwise, the name and id will default to "redirect"
    """

    form_name = kwargs.get('form_name', 'redirect')

    return_string="""
    <form action="fusebox.psp" name="%s" id="%s" method="post">
    """ % (form_name, form_name)

    for k, v in kwargs.iteritems():
        if k == 'form_name': continue
        return_string += '''
        <input type="hidden" name="%s" id="%s" value="%s">
        ''' % (k, k, v)

    return_string += '''</form>
    <script>document.forms['%s'].submit()</script>
    ''' % form_name

    return return_string
