import { store } from '@/services/ReduxStore/Store';
import { buildJsonApiPayload } from '@/utils/jsonapi';
import type { AxiosRequestConfig } from 'openapi-client-axios';
import { useEffect, useState } from 'react';
import { OpenAPIProvider } from 'react-openapi-client/OpenAPIProvider';
import { useOperationMethod } from 'react-openapi-client/useOperationMethod';
import { Provider as ReduxProvider } from 'react-redux';
import { getLocale, request, useIntl, useModel } from 'umi';
import PageLoading from '../PageLoading';


const axiosConfig: AxiosRequestConfig = {
  baseURL: '/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/vnd.api+json',
  }
};

const fetchSchema = async () => {
  try {
    return await request('/api/schema/', { method: 'GET'});
  } catch (error) {
  }
};

const setDjangoLanguageCookie = () => {
  let lang;
  switch(getLocale()){
    case 'de-DE':
      lang = 'de';
      break;
    case 'en-US':
    default:
      lang = 'en';
      break;
  }
  document.cookie = `django_language=${lang};path=/`;
};


const UserSettingsUpdater: React.FC = (props: any) => {
  const { initialState, initialState: { currentUser = undefined, settings = undefined } = {} } = useModel('@@initialState');
  const [updateUser, { error: updateUserError }] = useOperationMethod('updateUser');

  useEffect(() => {
    if (updateUserError){
      console.log('can not update user settings');
    }
  }, [updateUserError]);

  useEffect(() => {
    //FIXME: currently this will result in an initial patch, cause settings are set on getInitialState function...
    if (currentUser){
      updateUser(
        [{ name: 'id', value: currentUser.id, in: 'path' }],
        buildJsonApiPayload('User', currentUser.id, { settings: settings })
      );
    }
  }, [initialState, updateUser]);
  
  return (props.children);
}

/**
 * Workaround to init openapi provider before child containers are rendered
 * TODO: check if this can be simplyfied
 */
const RootContainer: React.FC = (props: any) => {
  const intl = useIntl();
  const [schema, setSchema] = useState();

  useEffect(() => {
    setDjangoLanguageCookie();
    
    const fetchSchemaAsync = async () => {
      setSchema(await fetchSchema());
    };
    fetchSchemaAsync();
  }, []);

  if (schema) {    
    return (
      <ReduxProvider store={store}>
        <OpenAPIProvider definition={schema} axiosConfigDefaults={axiosConfig}>
          <UserSettingsUpdater>
            {props.children}
          </UserSettingsUpdater>
        </OpenAPIProvider>
      </ReduxProvider>
    );    
  } else {
    return (
      <PageLoading
        title={intl.formatMessage({ id: 'component.rootContainer.loadingSchema' })}
        logo={<img alt="openapi logo" src="/openapi_logo.png" />}
      />
    );
  }
};

export default RootContainer;
