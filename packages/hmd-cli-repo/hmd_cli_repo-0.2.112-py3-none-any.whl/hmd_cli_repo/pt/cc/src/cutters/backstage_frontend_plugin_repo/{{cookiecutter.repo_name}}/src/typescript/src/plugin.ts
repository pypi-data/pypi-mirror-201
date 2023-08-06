import {
  createPlugin,
  createRoutableExtension,
} from '@backstage/core-plugin-api';

import { rootRouteRef } from './routes';

export const testPlugin = createPlugin({
  id: '{{ cookiecutter.short_name }}',
  routes: {
    root: rootRouteRef,
  },
});

export const TestPage = testPlugin.provide(
  createRoutableExtension({
    name: 'TestPage',
    component: () =>
      import('./components/ExampleComponent').then(
        (m) => m.ExampleComponent,
      ),
    mountPoint: rootRouteRef,
  }),
);
