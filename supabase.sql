-- Ejecutar una sola vez en SQL Editor de Supabase.
create table if not exists public.ley_estado (
 id integer primary key check (id=1),
 draft jsonb not null default '{}'::jsonb,
 published jsonb not null default '{}'::jsonb,
 promulgated boolean not null default false
);
insert into public.ley_estado (id) values (1) on conflict (id) do nothing;
alter table public.ley_estado enable row level security;
-- No se crean políticas públicas. Solo la service_role, guardada en Secrets
-- del servidor de Streamlit, puede leer o modificar esta tabla.
