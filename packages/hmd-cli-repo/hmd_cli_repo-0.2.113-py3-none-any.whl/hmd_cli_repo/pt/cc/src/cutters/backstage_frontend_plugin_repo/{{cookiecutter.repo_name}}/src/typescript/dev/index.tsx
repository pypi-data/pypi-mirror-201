import React from 'react';
import { createDevApp } from '@backstage/dev-utils';
import { testPlugin, TestPage } from '../src/plugin';

createDevApp()
  .registerPlugin(testPlugin)
  .addPage({
    element: <TestPage />,
    title: 'Root Page',
    path: '/test',
  })
  .render();
