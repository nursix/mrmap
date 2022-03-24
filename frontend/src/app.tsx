import RightContent from '@/components/RightContent';
import { GithubFilled, LinkOutlined } from '@ant-design/icons';
import type { Settings as LayoutSettings } from '@ant-design/pro-layout';
import { PageLoading, SettingDrawer } from '@ant-design/pro-layout';
import type { AxiosRequestConfig } from 'axios';
import React from 'react';
import { OpenAPIProvider } from 'react-openapi-client';
import type { RunTimeLayoutConfig } from 'umi';
import { history, Link, request } from 'umi';
import defaultSettings from '../config/defaultSettings';

const isDev = process.env.NODE_ENV === 'development';
const loginPath = '/user/login';

/**
 * This function will be executed once at the start of the application.
 * <p>
 * The return value is available globally via <code>useModel('@@initialState')</code>.
 * <p>
 * @see https://umijs.org/zh-CN/plugins/plugin-initial-state
 */
export async function getInitialState(): Promise<{
  settings?: Partial<LayoutSettings>;
  currentUser?: any;
  loading?: boolean;
  fetchUserInfo?: () => Promise<any | undefined>;
}> {
  const fetchUserInfo = async () => {
    try {
      const msg = await request<{
        data: any; // TODO: jsonapi response object as type
      }>('/api/v1/accounts/who-am-i/', {
        method: 'GET',
      });
      // who-am-i returns an AnonymousUser if no session can be found
      if (msg.data.attributes?.username !== 'AnonymousUser') {
        // TODO AvatarDropdown component supports avatar image, do we want this in our model?
        msg.data.attributes.avatar =
          'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png';
        return msg;
      }
    } catch (error) {
      history.push(loginPath);
    }
    return undefined;
  };
  // if this is not the login page, try to fetch user and set currentUser
  if (history.location.pathname !== loginPath) {
    const currentUser = await fetchUserInfo();
    return {
      fetchUserInfo,
      currentUser,
      settings: defaultSettings,
    };
  }
  return {
    fetchUserInfo,
    settings: defaultSettings,
  };
}

/** When obtaining the initial state is slow, this loading indicator will be visible. */
export const initialStateConfig = {
  loading: <PageLoading />,
};

// ProLayout api https://procomponents.ant.design/components/layout
export const layout: RunTimeLayoutConfig = ({ initialState, setInitialState }) => {
  return {
    rightContentRender: () => <RightContent />,
    disableContentMargin: false,
    waterMarkProps: {
      content: initialState?.currentUser?.name,
    },
    // footerRender: () => <Footer />,
    onPageChange: () => {
      const { location } = history;
      // if not logged in, redirect to login page
      if (!initialState?.currentUser && location.pathname !== loginPath) {
        history.push(loginPath);
      }
    },
    links: isDev
      ? [
          <Link key="openapi" to="/api/schema/" target="_blank">
            <LinkOutlined />
            <span>OpenAPI Schema</span>
          </Link>,
          <Link key="github" to="https://github.com/mrmap-community/mrmap" target="_blank">
            <GithubFilled />
            <span>Git</span>
          </Link>,
        ]
      : [],
    menuHeaderRender: undefined,
    // custom 403 page
    // unAccessible: <div>unAccessible</div>,
    childrenRender: (children, props) => {
      // add a loading state
      // if (initialState?.loading) return <PageLoading />;
      return (
        <>
          {children}
          {!props.location?.pathname?.includes('/login') && (
            <SettingDrawer
              disableUrlParams
              settings={initialState?.settings}
              onSettingChange={(settings) => {
                setInitialState((preInitialState: any) => ({
                  ...preInitialState,
                  settings,
                }));
              }}
            />
          )}
        </>
      );
    },
    ...initialState?.settings,
  };
};

const defaultConfig: AxiosRequestConfig = {
  baseURL: '/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/vnd.api+json',
  },
};

export function rootContainer(container: any) {
  return (
    <OpenAPIProvider definition="/api/schema/" axiosConfigDefaults={defaultConfig}>
      {container}
    </OpenAPIProvider>
  );
}
