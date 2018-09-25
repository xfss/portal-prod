import Vue from 'vue';
import Router from 'vue-router';
import get from 'lodash/get';

import Main from '@/components/Main';
import Login from '@/components/Login';
import Logout from '@/components/Logout';
import Unauthorized from '@/components/Unauthorized';
import Services from '@/components/Services';
import ServiceNew from '@/components/ServiceNew';
import ServiceEdit from '@/components/ServiceEdit';
import ServiceEvents from '@/components/ServiceEvents';
import FilesAdmin from '@/components/FilesAdmin';
import Files from '@/components/Files';
import FileUpload from '@/components/FileUpload';
import FileEdit from '@/components/FileEdit';
import FileEventsSingle from '@/components/FileEventsSingle';
import FileEvents from '@/components/FileEvents';
import Publications from '@/components/Publications';
import PublicationEdit from '@/components/PublicationEdit';
import Invoices from '@/components/Invoices';
import CreateInvoice from '@/components/invoices/CreateInvoice';

import store from '../store';

Vue.use(Router);

let router = new Router({
  mode: 'history',
  routes: [
    {path: '/', name: 'Main', component: Main, meta: {public: true}},
    {path: '/login', name: 'Login', component: Login, meta: {public: true}},
    {path: '/logout', name: 'Logout', component: Logout, meta: {public: true}},
    {path: '/unauthorized', name: 'Unauthorized', component: Unauthorized, meta: {public: true}},
    {path: '/service-new', name: 'New Service', component: ServiceNew, meta: {adminOnly: true}},
    {path: '/services', name: 'Services', component: Services},
    {path: '/services/:id', name: 'Edit Service', component: ServiceEdit, meta: {adminOnly: true}},
    {path: '/service-events', name: 'Service Events', component: ServiceEvents},
    {path: '/file-upload', name: 'File Upload', component: FileUpload},
    {path: '/files-admin', name: 'Files Admin', component: FilesAdmin},
    {path: '/files', name: 'Files', component: Files},
    {path: '/files/:id', name: 'Edit File', component: FileEdit},
    {path: '/files/:id/events', name: 'File Events', component: FileEventsSingle},
    {path: '/file-events', name: 'All File Events', component: FileEvents},
    {path: '/publication', name: 'Publications', component: Publications, meta: {publicationAdminOly: false}},
    {path: '/publication/:id', name: 'Edit Publication', component: PublicationEdit, meta: {publicationAdminOly: true}},
    {path: '/invoices', name: 'Invoices', component: Invoices},
    {path: '/invoices/create', name: 'Create Invoice', component: CreateInvoice}
  ]
});

router.beforeEach((to, from, next) => {
  let currentUser = get(store, ['getters', 'currentUser']);
  // Never redirect for login screen
  if (!to.matched.some((route) => { return route.name === 'Login'; })) {
    if (!to.matched.some((route) => { return route.meta.public; }) && (!get(currentUser, 'token') || !get(currentUser, ['data', 'is_active']))) {
      next({name: 'Login'});
      return;
    } else if (to.matched.some((route) => { return route.meta.adminOnly; }) && !get(currentUser, ['data', 'is_staff'], false)) {
      next({name: 'Unauthorized'});
      return;
    } else if (to.matched.some((route) => { return route.meta.publicationAdminOly; }) && !get(currentUser, ['data', 'is_publication_admin'], false)) {
      next({name: 'Unauthorized'});
      return;
    } else if (to.name === 'Main') {
      if (get(currentUser, 'token')) {
        next({name: 'File Upload'});
        return;
      } else {
        next({name: 'Login'});
        return;
      }
    }
  // Unless user already logged in
  } else {
    if (get(currentUser, 'token')) {
      next({name: 'File Upload'});
      return;
    }
  }
  next();
});

export {router};
export default router;
