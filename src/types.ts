export interface User {
  uuid: string;
  tg_id: number;
  firstName: string;
  lastName?: string | null;
  userName?: string | null;
  language_code?: string | null;
  is_premium?: string | null;
  allows_write_to_pm?: string | null;
  photo_url?: string | null;
}

export interface AuthContextInterface {
  user: User;
}
