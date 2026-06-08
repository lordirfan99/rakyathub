export interface AuthorInfo {
  id: string;
  name: string;
  title: string;
  bio: string;
  avatar: string;
  credentials: string;
  linkedin?: string;
  website?: string;
}

export const AUTHORS: Record<string, AuthorInfo> = {
  RakyatHub: {
    id: 'rakyathub',
    name: 'RakyatHub',
    title: 'Pakar Kewangan Digital Malaysia',
    bio: 'Pasukan RakyatHub',
    avatar: '/favicon.ico',
    credentials:
      'Penganalisis kewangan bertauliah dengan pengalaman dalam perancangan kewangan peribadi, pelaburan emas, KWSP, ASB, dan insurans. Aktif mengikuti perkembangan dasar kewangan negara dan bantuan kerajaan Malaysia.',
  },
};

export function getAuthor(key: string | undefined | null): AuthorInfo {
  if (key && AUTHORS[key]) return AUTHORS[key];
  return {
    id: 'rakyathub',
    name: key || 'RakyatHub',
    title: 'Pasukan RakyatHub',
    bio: '',
    avatar: '/favicon.ico',
    credentials: '',
  };
}
