sql_rls_owner_select_collaborators = """
    CREATE POLICY "Enable owner to select collaborators"
    ON public.account_instance
    FOR SELECT USING (
        is_instance_owner(auth.uid(), instance_id)
    );
"""  # noqa
