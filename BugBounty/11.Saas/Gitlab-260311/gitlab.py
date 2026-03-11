import os
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========== 配置区域 ==========
# 请替换为您的真实Cookie和CSRF令牌（从浏览器中复制）
COOKIE_STRING = "_gitlab_session=c02e757e6bb733a8d980c18e93644744; _cfuvid=Uk5huY8Cx5XNKHub0VpOcj6Jx2rfeB6Pg4I_DReV_Dc-1773211495558-0.0.1.1-604800000; super_sidebar_collapsed=false; _sp_ses.6b85=*; __cf_bm=LUCiMWoKMcdfRAApDwd4zCJwUTpEDQtP4pLVBU8bkx4-1773212484-1.0.1.1-6oCCcw9EKQl_z8Gocs6QTKVUnkpOQCjWE_tTOyy4o6UShLtUI_kyeiaIdjfM9nOfQy9Hjb9RR3VUb8iHVI9Z2V4VNApKG2ldWX9Cbj5M43E; _sp_id.6b85=327d9eba-46e2-486f-93a7-89c666e6c8b5.1773211504.1.1773212487..1650fb64-2be9-4f7b-b88c-b8e1a7b1c621..9de10f0a-fa94-4c41-a51a-516f7677d718.1773211504463.10"  # 完整Cookie字符串
X_CSRF_TOKEN = "XlwuiGKpoj8JThJf_4s1wYtYvIjgR23D-Li0dUFXaDiUYaqkHPdOkXBVonksyLoAinM9DPI6ubOYT0nGWDQtTA"

# GraphQL API端点
URL = "https://gitlab.com/api/graphql"

# 请求头模板（请根据需要修改其他字段）
HEADERS_TEMPLATE = {
    "Host": "gitlab.com",
    "Cookie": COOKIE_STRING,
    "X-Csrf-Token": X_CSRF_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://gitlab.com",
    "Referer": "https://gitlab.com/gitlab-org/gitlab/-/work_items",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Sec-Ch-Ua": '"Chromium";v="145", "Not:A-Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Priority": "u=1,1",
}

# 重试策略（避免网络波动）
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# ========== GraphQL 查询模板 ==========
# 第一个请求：搜索工作项列表
QUERY_LIST = """
query getWorkItemsSlimEE($excludeProjects: Boolean = false, $excludeGroupWorkItems: Boolean = false, $includeDescendants: Boolean = true, $iid: String, $fullPath: ID!, $search: String, $sort: WorkItemSort, $state: IssuableState, $assigneeWildcardId: AssigneeWildcardId, $assigneeUsernames: [String!], $authorUsername: String, $closedAfter: Time, $closedBefore: Time, $confidential: Boolean, $createdAfter: Time, $createdBefore: Time, $dueAfter: Time, $dueBefore: Time, $labelName: [String!], $milestoneTitle: [String!], $milestoneWildcardId: MilestoneWildcardId, $myReactionEmoji: String, $subscribed: SubscriptionStatus, $types: [IssueType!], $updatedAfter: Time, $updatedBefore: Time, $crmOrganizationId: String, $crmContactId: String, $customField: [WorkItemWidgetCustomFieldFilterInputType!], $weight: String, $weightWildcardId: WeightWildcardId, $healthStatusFilter: HealthStatusFilter, $status: WorkItemWidgetStatusFilterInput, $releaseTag: [String!], $releaseTagWildcardId: ReleaseTagWildcardId, $iterationId: [ID], $iterationWildcardId: IterationWildcardId, $iterationCadenceId: [IterationsCadenceID!], $hierarchyFilters: HierarchyFilterInput, $in: [IssuableSearchableField!], $not: NegatedWorkItemFilterInput, $or: UnionedWorkItemFilterInput, $afterCursor: String, $beforeCursor: String, $firstPageSize: Int, $lastPageSize: Int, $useWorkItemFeatures: Boolean = false) {
  namespace(fullPath: $fullPath) {
    id
    name
    workItems(
      iid: $iid
      excludeProjects: $excludeProjects
      excludeGroupWorkItems: $excludeGroupWorkItems
      includeDescendants: $includeDescendants
      search: $search
      sort: $sort
      state: $state
      assigneeUsernames: $assigneeUsernames
      assigneeWildcardId: $assigneeWildcardId
      authorUsername: $authorUsername
      closedAfter: $closedAfter
      closedBefore: $closedBefore
      confidential: $confidential
      createdAfter: $createdAfter
      createdBefore: $createdBefore
      dueBefore: $dueBefore
      dueAfter: $dueAfter
      labelName: $labelName
      milestoneTitle: $milestoneTitle
      milestoneWildcardId: $milestoneWildcardId
      myReactionEmoji: $myReactionEmoji
      subscribed: $subscribed
      types: $types
      updatedAfter: $updatedAfter
      updatedBefore: $updatedBefore
      crmOrganizationId: $crmOrganizationId
      crmContactId: $crmContactId
      customField: $customField
      weight: $weight
      weightWildcardId: $weightWildcardId
      healthStatusFilter: $healthStatusFilter
      status: $status
      releaseTag: $releaseTag
      releaseTagWildcardId: $releaseTagWildcardId
      iterationId: $iterationId
      iterationWildcardId: $iterationWildcardId
      iterationCadenceId: $iterationCadenceId
      hierarchyFilters: $hierarchyFilters
      in: $in
      not: $not
      or: $or
      after: $afterCursor
      before: $beforeCursor
      first: $firstPageSize
      last: $lastPageSize
    ) {
      pageInfo {
        ...PageInfo
        __typename
      }
      nodes {
        id
        author {
          ...User
          __typename
        }
        closedAt
        createdAt
        iid
        namespace {
          id
          fullPath
          __typename
        }
        reference(full: true)
        title
        updatedAt
        webUrl
        webPath @gl_introduced(version: "18.6.0-pre")
        state
        widgets(onlyTypes: [LABELS]) {
          type
          ... on WorkItemWidgetLabels {
            allowsScopedLabels
            labels {
              nodes {
                ...Label
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        features @include(if: $useWorkItemFeatures) {
          labels {
            allowsScopedLabels
            labels {
              nodes {
                ...Label
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        workItemType {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment PageInfo on PageInfo {
  hasNextPage
  hasPreviousPage
  startCursor
  endCursor
  __typename
}

fragment User on User {
  id
  avatarUrl
  name
  username
  webUrl
  webPath
  __typename
}

fragment Label on Label {
  id
  title
  description
  color
  textColor
  __typename
}
"""

# 第二个请求：获取单个工作项详情
QUERY_ITEM = """
query namespaceWorkItem($fullPath: ID!, $iid: String!, $useWorkItemFeatures: Boolean = false) {
  namespace(fullPath: $fullPath) {
    id
    workItem(iid: $iid) {
      ...WorkItem
      __typename
    }
    __typename
  }
}

fragment WorkItem on WorkItem {
  id
  iid
  archived
  externalAuthor
  hidden
  imported
  title
  titleHtml
  state
  description
  confidential
  createdAt
  closedAt
  userDiscussionsCount
  webUrl
  reference(full: true)
  createNoteEmail
  promotedToEpicUrl
  movedToWorkItemUrl
  duplicatedToWorkItemUrl
  showPlanUpgradePromotion
  project {
    id
    __typename
  }
  namespace {
    id
    fullPath
    name
    fullName
    webUrl
    __typename
  }
  author {
    ...Author
    __typename
  }
  workItemType {
    id
    name
    iconName
    __typename
  }
  userPermissions {
    ...WorkItemPermissions
    __typename
  }
  commentTemplatesPaths {
    text
    href
    __typename
  }
  widgets {
    ...WorkItemWidgets
    __typename
  }
  features @include(if: $useWorkItemFeatures) {
    ...WorkItemFeatures
    __typename
  }
  __typename
}

fragment Author on User {
  id
  avatarUrl
  name
  username
  webUrl
  webPath
  __typename
}

fragment WorkItemWidgets on WorkItemWidget {
  type
  ...BaseWorkItemWidgets
  ... on WorkItemWidgetLabels {
    allowsScopedLabels
    labels {
      nodes {
        ...Label
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetStartAndDueDate {
    dueDate
    startDate
    rollUp
    isFixed
    __typename
  }
  ... on WorkItemWidgetWeight {
    weight
    rolledUpWeight
    rolledUpCompletedWeight
    widgetDefinition {
      editable
      rollUp
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetProgress {
    progress
    updatedAt
    __typename
  }
  ... on WorkItemWidgetIteration {
    iteration {
      id
      title
      startDate
      dueDate
      webUrl
      iterationCadence {
        id
        title
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetHealthStatus {
    healthStatus
    rolledUpHealthStatus {
      count
      healthStatus
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetColor {
    color
    textColor
    __typename
  }
  ... on WorkItemWidgetLinkedItems {
    blockedByCount
    blockingCount
    __typename
  }
  ... on WorkItemWidgetCustomFields {
    customFieldValues {
      customField {
        id
        name
        fieldType
        __typename
      }
      ... on WorkItemNumberFieldValue {
        value
        __typename
      }
      ... on WorkItemTextFieldValue {
        value
        __typename
      }
      ... on WorkItemSelectFieldValue {
        selectedOptions {
          id
          value
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetStatus {
    status {
      ...WorkItemStatusFragment
      __typename
    }
    __typename
  }
  __typename
}

fragment WorkItemStatusFragment on WorkItemStatus {
  id
  category
  color
  description
  iconName
  name
  position
  __typename
}

fragment BaseWorkItemWidgets on WorkItemWidget {
  type
  ... on WorkItemWidgetAssignees {
    allowsMultipleAssignees
    canInviteMembers
    assignees {
      nodes {
        ...User
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetCrmContacts {
    contactsAvailable
    contacts {
      nodes {
        id
        email
        firstName
        lastName
        phone
        description
        organization {
          id
          name
          description
          defaultRate
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetCurrentUserTodos {
    currentUserTodos(state: pending) {
      nodes {
        id
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetDescription {
    description
    descriptionHtml
    lastEditedAt
    lastEditedBy {
      name
      webPath
      __typename
    }
    taskCompletionStatus {
      completedCount
      count
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetErrorTracking {
    identifier
    __typename
  }
  ... on WorkItemWidgetHierarchy {
    hasChildren
    hasParent
    rolledUpCountsByType {
      countsByState {
        opened
        all
        closed
        __typename
      }
      workItemType {
        id
        name
        iconName
        __typename
      }
      __typename
    }
    parent {
      id
      iid
      title
      confidential
      namespace {
        id
        fullPath
        __typename
      }
      webUrl
      workItemType {
        id
        name
        iconName
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetLabels {
    labels {
      nodes {
        ...Label
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetLinkedResources {
    linkedResources {
      nodes {
        url
        __typename
      }
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetMilestone {
    milestone {
      ...MilestoneFragment
      __typename
    }
    __typename
  }
  ... on WorkItemWidgetNotes {
    discussionLocked
    __typename
  }
  ... on WorkItemWidgetStartAndDueDate {
    dueDate
    startDate
    rollUp
    __typename
  }
  ... on WorkItemWidgetTimeTracking {
    timeEstimate
    humanReadableAttributes {
      timeEstimate
      __typename
    }
    timelogs {
      nodes {
        ...TimelogFragment
        __typename
      }
      __typename
    }
    totalTimeSpent
    __typename
  }
  __typename
}

fragment Label on Label {
  id
  title
  description
  color
  textColor
  __typename
}

fragment User on User {
  id
  avatarUrl
  name
  username
  webUrl
  webPath
  __typename
}

fragment MilestoneFragment on Milestone {
  expired
  id
  title
  state
  startDate
  dueDate
  webPath
  projectMilestone
  __typename
}

fragment TimelogFragment on WorkItemTimelog {
  __typename
  id
  timeSpent
  user {
    id
    name
    __typename
  }
  spentAt
  note {
    id
    body
    __typename
  }
  summary
  userPermissions {
    adminTimelog
    __typename
  }
}

fragment WorkItemPermissions on WorkItemPermissions {
  adminParentLink
  adminWorkItemLink
  createNote
  deleteWorkItem
  markNoteAsInternal
  moveWorkItem
  reportSpam
  setWorkItemMetadata
  summarizeComments
  updateWorkItem
  blockedWorkItems
  __typename
}

fragment WorkItemFeatures on WorkItemFeatures {
  description {
    description
    descriptionHtml
    lastEditedAt
    lastEditedBy {
      name
      webPath
      __typename
    }
    taskCompletionStatus {
      completedCount
      count
      __typename
    }
    __typename
  }
  assignees {
    allowsMultipleAssignees
    assignees {
      nodes {
        id
        avatarUrl
        name
        username
        webUrl
        webPath
        __typename
      }
      __typename
    }
    __typename
  }
  awardEmoji {
    upvotes
    downvotes
    __typename
  }
  milestone {
    milestone {
      id
      dueDate
      startDate
      title
      webPath
      __typename
    }
    __typename
  }
  startAndDueDate {
    startDate
    dueDate
    rollUp
    isFixed
    __typename
  }
  timeTracking {
    humanReadableAttributes {
      timeEstimate
      __typename
    }
    __typename
  }
  healthStatus {
    healthStatus
    __typename
  }
  weight {
    weight
    __typename
  }
  linkedItems {
    blockedByCount
    blockingCount
    __typename
  }
  iteration {
    iteration {
      id
      title
      startDate
      dueDate
      webUrl
      iterationCadence {
        id
        title
        __typename
      }
      __typename
    }
    __typename
  }
  development {
    closingMergeRequests {
      count
      __typename
    }
    __typename
  }
  hierarchy {
    parent {
      id
      __typename
    }
    __typename
  }
  status {
    ...WorkItemFeatureStatus
    __typename
  }
  __typename
}

fragment WorkItemFeatureStatus on WorkItemWidgetStatus {
  status {
    id
    category
    color
    description
    iconName
    name
    position
    __typename
  }
  __typename
}
"""

def read_search_terms(filename="name.txt"):
    """读取name.txt中的搜索词，每行一个，返回列表"""
    if not os.path.exists(filename):
        print(f"错误：文件 {filename} 不存在，请创建并写入搜索词（每行一个）")
        return []
    with open(filename, "r", encoding="utf-8") as f:
        terms = [line.strip() for line in f if line.strip()]
    return terms

def send_graphql_request(query, variables, headers):
    """发送GraphQL请求，返回JSON响应"""
    payload = {
        "operationName": None,  # 实际查询中包含operationName，但这里不强制
        "query": query,
        "variables": variables
    }
    try:
        resp = session.post(URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except json.JSONDecodeError:
        print("响应不是有效的JSON")
        return None

def extract_iids_from_list_response(data):
    """从第一个请求的响应中提取所有iid"""
    iids = []
    try:
        nodes = data["data"]["namespace"]["workItems"]["nodes"]
        for node in nodes:
            iid = node.get("iid")
            if iid:
                iids.append(iid)
    except (KeyError, TypeError) as e:
        print(f"解析iid列表失败: {e}")
    return iids

def extract_description_from_item_response(data):
    """从第二个请求的响应中提取description"""
    try:
        return data["data"]["namespace"]["workItem"]["description"]
    except (KeyError, TypeError):
        return None

def save_description(search_term, iid, description):
    """将description保存到文件 search_term/iid.md"""
    dir_path = os.path.join(os.getcwd(), search_term)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{iid}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(description if description else "")
    print(f"已保存: {file_path}")

def main():
    # 检查必要的认证信息
    if COOKIE_STRING == "_gitlab_session=your_session_value; ..." or X_CSRF_TOKEN == "your_x_csrf_token_value":
        print("请先在脚本开头配置有效的Cookie和X-Csrf-Token！")
        return

    headers = HEADERS_TEMPLATE.copy()
    # 确保Cookie字符串是有效的
    headers["Cookie"] = COOKIE_STRING
    headers["X-Csrf-Token"] = X_CSRF_TOKEN

    search_terms = read_search_terms()
    if not search_terms:
        print("未找到搜索词，退出。")
        return

    total_terms = len(search_terms)
    for idx, term in enumerate(search_terms, 1):
        print(f"\n[{idx}/{total_terms}] 正在处理搜索词: {term}")
        # 第一个请求
        list_vars = {
            "fullPath": "gitlab-org/gitlab",
            "search": term,
            "firstPageSize": 10000,
            "sort": "CREATED_DESC",
            "state": "all",
            "types": ["ISSUE", "INCIDENT", "TASK", "TICKET", "EPIC", "KEY_RESULT", "OBJECTIVE", "TEST_CASE"],
            "excludeProjects": False,
            "excludeGroupWorkItems": False,
            "includeDescendants": True,
            "useWorkItemFeatures": False
        }
        print(f"  发送列表请求...")
        list_resp = send_graphql_request(QUERY_LIST, list_vars, headers)
        if not list_resp:
            print(f"  跳过搜索词 {term}")
            continue

        iids = extract_iids_from_list_response(list_resp)
        if not iids:
            print(f"  未找到任何工作项，跳过。")
            continue

        print(f"  找到 {len(iids)} 个工作项，开始获取详情...")
        for i, iid in enumerate(iids, 1):
            print(f"    [{i}/{len(iids)}] 获取工作项 {iid} ...")
            item_vars = {
                "fullPath": "gitlab-org/gitlab",
                "iid": iid,
                "useWorkItemFeatures": False
            }
            item_resp = send_graphql_request(QUERY_ITEM, item_vars, headers)
            if not item_resp:
                print(f"      请求失败，跳过")
                continue
            description = extract_description_from_item_response(item_resp)
            if description is None:
                print(f"      未找到description字段，可能响应结构异常")
                # 可以打印完整响应调试，但这里跳过
                continue
            save_description(term, iid, description)
            # 适当延时，避免请求过频
            time.sleep(0.5)

        # 每个搜索词之间稍长延时
        time.sleep(1)

    print("\n所有任务完成！")

if __name__ == "__main__":
    main()