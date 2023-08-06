import requests
import time
import json

class Gitlab:

  DEFAULT_PAGE_SIZE = 100

  def __init__(self, token, base_url="https://gitlab.com/"):
    self.token = token
    self.base_url = base_url
    self.api_url = "api/v4/"
    self.request_headers = {
      "PRIVATE-TOKEN": self.token,
      "Content-Type": "application/json"
    }

  ### API METHODS ###

  def list_generic(self, path, page, page_size):
    response = requests.get(
      f'{self.base_url}{self.api_url}{path}?per_page={page_size}&page={page}', 
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code,
    }

  def list_groups(self):
    return self.get_paginated_list_generic('groups')

  def list_sub_groups(self, id):
    return self.get_paginated_list_generic(f'groups/{id}/subgroups')

  def list_group_projects(self, id):
    return self.get_paginated_list_generic(f'groups/{id}/projects')

  def create_group(self, path, parent_id = None):
    
    body = {
      "name": str(path.replace('-', ' ').title()),
      "path": str(path)
    }

    if parent_id is not None:
      body['parent_id'] = str(parent_id)

    response = requests.post(
      f'{self.base_url}{self.api_url}groups', 
      headers=self.request_headers, 
      data=json.dumps(body)
    )
    return {'status_code': response.status_code}

  def create_project(self, path, namespace_id):
    
    body = {
      "name": str(path.replace('-', ' ').title()),
      "path": str(path),
      "namespace_id": str(namespace_id),
    }

    response = requests.post(
      f'{self.base_url}{self.api_url}projects',
      headers=self.request_headers,
      data=json.dumps(body)
    )
    return {'status_code': response.status_code}

  def delete_project(self, project_id):

    response = requests.delete(
      f'{self.base_url}{self.api_url}projects/{project_id}', 
      headers=self.request_headers
    )
    return {'status_code': response.status_code}

  def get_project(self, project_id):

    response = requests.get(
      f'{self.base_url}{self.api_url}projects/{project_id}', 
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code,
    }

  def unprotect_branch(self, project_id, branch_name='main'):

    response = requests.delete(
      f'{self.base_url}{self.api_url}projects/{project_id}/protected_branches/{branch_name}', 
      headers=self.request_headers
    )
    return {'status_code': response.status_code}

  def create_branch(self, project_id, branch_name, branch_ref):

    response = requests.post(
      f'{self.base_url}{self.api_url}projects/{project_id}/repository/branches?branch={branch_name}&ref={branch_ref}', 
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code,
    }

  def get_branch(self, project_id, branch_name):

    response = requests.get(
      f'{self.base_url}{self.api_url}projects/{project_id}/repository/branches/{branch_name}', 
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code,
    }

  def get_paginated_list_generic(self, path, page = 1, page_size = DEFAULT_PAGE_SIZE, previous_pages = []):
    current_page = self.list_generic(path, page, page_size)['text']
    pages = current_page

    try:
      pages = previous_pages + current_page
    except TypeError:
      pass

    if len(current_page) == page_size:
      return self.get_paginated_list_generic(path, page + 1, page_size, pages)
    else:
      return pages

  def create_pages_domain(self, project_id, domain, auto_ssl_enabled = True):

    body = {
      "domain": str(domain),
      "auto_ssl_enabled": auto_ssl_enabled,
    }

    response = requests.post(
      f'{self.base_url}{self.api_url}projects/{project_id}/pages/domains',
      headers=self.request_headers,
      data=json.dumps(body)
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code
    }

  def list_pages_domain(self, project_id):

    response = requests.get(
      f'{self.base_url}{self.api_url}projects/{project_id}/pages/domains',
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code
    }

  def trigger_pipeline(self, project_id, ref='main'):

    response = requests.post(
      f'{self.base_url}{self.api_url}projects/{project_id}/pipeline?ref={ref}',
      headers=self.request_headers,
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code
    }

  def create_pages_domain_if_available(self, project_id, domain, auto_ssl_enabled = True):

    print('--- BUILDING PAGES ---')
    pages_create = self.create_pages_domain(project_id, domain, auto_ssl_enabled)

    if pages_create['status_code'] == 404:
      print(f"--- {pages_create['text']['message']}")
      print('--- FINISHED PAGES ---')
      return 'N/A'

    if pages_create['status_code'] == 400:
      print(f"--- Domain {domain} is already taken")
      pages_list = self.list_pages_domain(project_id)['text']

      for page in pages_list:
        if page['domain'] == domain:
          print(f"--- Verification code is {page['verification_code']}")
          print('--- FINISHED PAGES ---')
          return page['verification_code']
      
      print(f"--- Domain {domain} does not belong to this project")
      print('--- FINISHED PAGES ---')
      return 'N/A'

    print(f"--- Verification code is {pages_create['text']['verification_code']}")
    print('--- FINISHED PAGES ---')
    return pages_create['text']['verification_code']

  def get_latest_pipeline(self, project_id):

    response = requests.get(
      f'{self.base_url}{self.api_url}projects/{project_id}/pipelines/latest',
      headers=self.request_headers
    )
    return {
      'text': json.loads(response.text),
      'status_code': response.status_code
    }

  ### LOGIC CALLS ###

  def get_groups(self, parent_id = None):
    return self.list_groups() if parent_id is None else self.list_sub_groups(parent_id)

  def find_object_by_path(self, path, array_of_objs):
    for obj in array_of_objs:
      if obj['path'] == path:
        return obj

    return []

  def find_base_group_by_path(self, path, array_of_objs):
    for obj in array_of_objs:
      if obj['path'] == path and obj['full_path'] == path :
        return obj

    return []

  def build_request_chain(self, full_path):

    print(f'--- BUILDING FOR {full_path} ---')

    paths = full_path.split('/')
    try:
      parent_id = self.find_base_group_by_path(paths[0], self.get_groups())['id']

    except Exception as ex:
      print(ex)
      raise Exception('Check path, check if user has permissions to repo')

    for path in paths[1:-1]:
      parent_id = self.build_group(path, parent_id)['id']

    projs = paths[-1].split('+')
    projs_ids = []
    for path in projs:
      proj = self.build_project(path, parent_id)
      projs_ids.append(proj["id"])

    print(f'--- FINISHED BUILDING ---')
    return projs_ids

  def build_group(self, path, parent_id):
    group = self.find_object_by_path(path, self.get_groups(parent_id))

    if not group:
      print(f'--- CREATE GROUP -> {path} PARENT ID: {parent_id}')
      try:
        self.create_group(path, parent_id)
      except Exception as e:
        print('>>> Issue is most likely due to a project or group with the same name at the same level! <<<')
        raise e
      group = self.find_object_by_path(path, self.get_groups(parent_id))
    else:
      print(f'--- GROUP EXISTS -> {path} WITH ID: {group["id"]} AND PARENT ID: {parent_id}')

    return group

  def build_project(self, path, parent_id):
    proj = self.find_object_by_path(path, self.list_group_projects(parent_id))

    if not proj:
      print(f'--- CREATE PRJCT -> {path} WITH PARENT ID: {parent_id}')
      try:
        self.create_project(path, parent_id)
      except Exception as e:
        print('>>> Issue is most likely due to a project or group with the same name at the same level! <<<')
        raise e
      proj = self.find_object_by_path(path, self.list_group_projects(parent_id))

      print(f'--- CREATE BRANCH MAIN FOR PRJCT -> {path} WITH ID: {proj["id"]}')
      self.create_branch(proj["id"], 'main', 'main')

      print(f'--- UNPROTECTING BRANCH MAIN -> {path} {proj["id"]}')
      self.unprotect_branch(proj["id"])

    else:
      print(f'--- PRJCT EXISTS -> {path} WITH ID: {proj["id"]} AND PARENT ID: {parent_id}')

    return proj

  def wait_for_latest_pipeline(self, project_id):

    print(f"Waiting for Pipeline with PROJECT ID:{project_id} started")

    final_states = ['success', 'failed', 'canceled', 'skipped']
    status_codes = [400, 401, 403, 404, 500, 503]

    response = self.get_latest_pipeline(project_id)

    if response['status_code'] in status_codes:
      print(response['text']['message'])
      return response['text']['message']

    while(True):
      time.sleep(5)

      if response['text']['status'] in final_states:
        break

      response = self.get_latest_pipeline(project_id)
      print(f"Checking Pipeline with PROJECT ID:{project_id}...")
   
    print(f"Pipeline has finished with {response['text']['status']} state")
    return response['text']