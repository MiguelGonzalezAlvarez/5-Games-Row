import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = supabaseUrl && supabaseAnonKey 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: number;
          email: string;
          username: string;
          avatar_url: string | null;
          created_at: string;
        };
        Insert: {
          email: string;
          username: string;
          avatar_url?: string | null;
        };
      };
      posts: {
        Row: {
          id: number;
          user_id: number;
          image_url: string;
          caption: string | null;
          likes_count: number;
          created_at: string;
        };
        Insert: {
          user_id: number;
          image_url: string;
          caption?: string | null;
        };
      };
    };
  };
}

export async function signUp(email: string, password: string) {
  if (!supabase) throw new Error('Supabase not configured');
  return supabase.auth.signUp({ email, password });
}

export async function signIn(email: string, password: string) {
  if (!supabase) throw new Error('Supabase not configured');
  return supabase.auth.signInWithPassword({ email, password });
}

export async function signOut() {
  if (!supabase) throw new Error('Supabase not configured');
  return supabase.auth.signOut();
}

export async function getSession() {
  if (!supabase) throw new Error('Supabase not configured');
  return supabase.auth.getSession();
}

export function subscribeToAuthChanges(callback: (event: string, session: any) => void) {
  if (!supabase) throw new Error('Supabase not configured');
  return supabase.auth.onAuthStateChange(callback);
}
