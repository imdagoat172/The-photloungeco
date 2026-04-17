import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Services } from './services/services';
import { Faq } from './faq/faq';
import { Contact } from './contact/contact';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'services', component: Services },
  { path: 'faq', component: Faq },
  { path: 'contact', component: Contact },
  { path: '**', redirectTo: '' }
];
