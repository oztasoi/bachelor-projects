const constants = {
  NODE_ENV: "dev",
  CLIENT_ACTIVE_DURATION: 60000,
  ENUMS: {
    CLIENT_TYPE: {
      CUSTOMER: "Customer",
      VENDOR: "Vendor",
      ADMIN: "Admin",
    },
    STATUS: {
      PENDING: "PENDING",
      ACCEPTED: "ACCEPTED",
      DECLINED: "DECLINED",
    },
  },
  LANGUAGE: {
    EN: "en",
    TR: "tr",
  },
  RESPONSE: {
    CODE: "returnCode",
    MESSAGE: "returnMessage",
    TITLE: "returnTitle",
    ICON: "iconName",
  },
  DAYS: {
    en: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  },
  ACTOR_URLS: {
    CUSTOMER: "/customer",
    VENDOR: "/vendor",
  },
  OBJECTIVES: {
    GET_CATEGORY: "Get all categories.",
    POST_CATEGORY: "Create a category.",
    GET_CATEGORY_ID: "Get a category.",
    PATCH_CATEGORY_ID: "Update a category.",
    DELETE_CATEGORY_ID: "Delete a category.",
    GET_SHOPPINGLIST_ALL: "Get all shoppinglists.",
    DELETE_SHOPPINGLIST_ALL: "Delete all shoppinglists.",
    POST_A_SHOPPINGLIST: "Create a shoppinglist.",
    GET_SHOPPINGLIST_ID: "Get a shoppinglist.",
    PATCH_SHOPPINGLIST_ID: "Update a shoppinglist.",
    DELETE_SHOPPINGLIST_ID: "Delete a shoppinglist.",
    POST_SHOPPINGLIST_ALL_EXPORT: "Export all shoppinglists into shoppingcart.",
    POST_SHOPPINGLIST_ID_EXPORT: "Export a shoppinglist into shoppingcart.",
    POST_CUSTOMER_SIGNUP: "Sign up.",
    POST_CUSTOMER_LOGIN: "Login.",
    POST_CUSTOMER_LOGOUT: "Logout.",
    GET_CUSTOMER_VERIFYEMAIL: "Verify registration email.",
    POST_CUSTOMER_CHANGEPASSWORD: "Request change password.",
    POST_CUSTOMER_FORGOTPASSWORD: "Request forgot password.",
    POST_CUSTOMER_RESETPASSWORD: "Request reset password.",
    PATCH_CUSTOMER_ME: "Update profile information.",
    GET_CUSTOMER_ME: "Retrieve profile information.",
    DELETE_CUSTOMER_ME: "Delete client.",
    GET_CUSTOMER: "Get all customers.",
    GET_CUSTOMER_ID: "Get a customer.",
    PATCH_CUSTOMER_ID: "Patch a customer.",
    DELETE_CUSTOMER_ID: "Delete a customer.",
    POST_VENDOR_SIGNUP: "Sign up.",
    POST_VENDOR_LOGIN: "Login.",
    POST_VENDOR_LOGOUT: "Logout.",
    GET_VENDOR_VERIFYEMAIL: "Verify registration email.",
    POST_VENDOR_CHANGEPASSWORD: "Request change password.",
    POST_VENDOR_FORGOTPASSWORD: "Request forgot password.",
    POST_VENDOR_RESETPASSWORD: "Request reset password.",
    PATCH_VENDOR_ME: "Update profile information.",
    GET_VENDOR_ME: "Retrieve profile information.",
    DELETE_VENDOR_ME: "Delete client.",
    GET_VENDOR: "Get all vendors.",
    GET_VENDOR_PUBLIC_ID: "Get a vendor information.",
    POST_VENDOR_ID: "Post vendor id.",
    GET_VENDOR_ME_PRODUCT: "Get vendor's all products.",
    GET_VENDOR_ME_PRODUCT_ID: "Get vendor's a product.",
    PATCH_VENDOR_ME_PRODUCT_ID: "Update vendor's a product.",
    DELETE_VENDOR_ME_PRODUCT_ID: "Delete vendor's a product.",
    GET_VENDOR_ME_MAINPRODUCT: "Get a vendor's all main products.",
    DELETE_VENDOR_ME_MAINPRODUCT_ID: "Delete vendor's a main product.",
    POST_VENDOR_ME_PRODUCT_NEW: "Post a vendor's new product.",
    POST_VENDOR_ME_PRODUCT_EXISTING_ID: "Post a vendor's new product from existing one.",
    GET_VENDOR_ME_PRODUCT_REQUEST: "Get vendor's all product requests.",
    GET_VENDOR_ME_PRODUCT_REQUEST_ID: "Get vendor's a product request.",
    PATCH_VENDOR_ME_PRODUCT_REQUEST_ID: "Update vendor's a product request.",
    DELETE_VENDOR_ME_PRODUCT_REQUEST_ID: "Delete vendor's a product request.",
    GET_COMMENT_ID_ALL: "Get all comments for a product.",
    GET_COMMENT_ID: "Get all comments for a product from a customer.",
    POST_COMMENT_ID: "Create a comment for a product from a customer.",
    PATCH_COMMENT_ID: "Update a comment for a product from a customer.",
    DELETE_COMMENT_ID: "Delete a comment for a product from a customer.",
    GET_PRODUCT: "Retrieve all products.",
    POST_PRODUCT: "Create a product.",
    GET_PRODUCT_ID: "Get a product.",
    POST_PRODUCT_ID: "Create a product.",
    PATCH_PRODUCT_ID: "Update a product.",
    DELETE_PRODUCT_ID: "Delete a product.",
    PATCH_PRODUCT_ID_VENDOR_ID: "Update a product of a vendor.",
    DELETE_PRODUCT_ID_VENDOR_ID: "Delete a product of a vendor.",
    POST_PRODUCT_SEARCH: "Search a product.",
    POST_PRODUCT_SEARCHFILTERS: "Push search parameters.",
    GET_MAINPRODUCT: "Get all mainproducts.",
    POST_MAINPRODUCT: "Create a mainproduct.",
    GET_MAINPRODUCT_ID: "Get a mainproduct.",
    PATCH_MAINPRODUCT_ID: "Update a mainproduct.",
    DELETE_MAINPRODUCT_ID: "Delete a mainproduct.",
    DELETE_MAINPRODUCT_ID_VENDOR_ID: "Delete a mainproduct from a vendor.",
    GET_PRODUCTREQUEST: "Get all productrequests.",
    GET_PRODUCTREQUEST_ID: "Get a productrequest.",
    POST_PRODUCTREQUEST_ID: "Create a product.",
    DELETE_PRODUCTREQUEST_ID: "Delete a product.",
    GET_TICKET: "Get all tickets.",
    POST_TICKET: "Create a ticket.",
    GET_TICKET_ID: "Get a ticket.",
    POST_TICKET_ID: "Reply a ticket.",
    PATCH_TICKET_ID: "Forward a ticket.",
    DELETE_TICKET_ID: "Delete a ticket.",
    GET_TICKET_ALL: "Get all active tickets.",
    GET_TICKET_ALL_UNASSIGNED: "Get all active unassigned tickets",
    GET_TICKET_ADMIN_ID: "Get all tickets of an admin.",
    GET_TICKET_ALL_ADMIN_ID: "Get all active tickets of an admin.",
    GET_TICKET_CLIENT_ID: "Get all tickets of a client.",
    GET_TICKET_ALL_CLIENT_ID: "Get all active tickets of a client.",
    GET_TICKET_ADMIN_ID_CLIENT_ID: "Get all tickets between an admin and a client.",
    GET_TICKET_ALL_ADMIN_ID_CLIENT_ID: "Get all active tickets between an admin and a client.",
    GET_SHOPPINGLIST_WATCHLIST: "Get one's watchlist.",
    POST_SHOPPINGLIST_WATCHLIST: "Add product to one's watchlist.",
    DELETE_SHOPPINGLIST_WATCHLIST: "Remove product to one's watchlist.",
    GET_CUSTOMER_NOTIFICATION: "Get one's notifications",
    POST_CUSTOMER_NOTIFICATION: "Read one notification of customer.",
    GET_VENDOR_NOTIFICATION: "Get one's notifications",
    POST_VENDOR_NOTIFICATION: "Read one notification of vendor.",
  },
  EVENT_IDS: {
    GET_CATEGORY: 1,
    POST_CATEGORY: 2,
    GET_CATEGORY_ID: 3,
    PATCH_CATEGORY_ID: 4,
    DELETE_CATEGORY_ID: 5,
    GET_SHOPPINGLIST_ALL: 6,
    DELETE_SHOPPINGLIST_ALL: 7,
    POST_A_SHOPPINGLIST: 8,
    GET_SHOPPINGLIST_ID: 9,
    PATCH_SHOPPINGLIST_ID: 10,
    DELETE_SHOPPINGLIST_ID: 11,
    POST_SHOPPINGLIST_ALL_EXPORT: 12,
    POST_SHOPPINGLIST_ID_EXPORT: 13,
    POST_CUSTOMER_SIGNUP: 14,
    POST_CUSTOMER_LOGIN: 15,
    POST_CUSTOMER_LOGOUT: 16,
    GET_CUSTOMER_VERIFYEMAIL: 17,
    POST_CUSTOMER_CHANGEPASSWORD: 18,
    POST_CUSTOMER_FORGOTPASSWORD: 19,
    POST_CUSTOMER_RESETPASSWORD: 20,
    PATCH_CUSTOMER_ME: 21,
    GET_CUSTOMER_ME: 22,
    DELETE_CUSTOMER_ME: 23,
    GET_CUSTOMER: 24,
    GET_CUSTOMER_ID: 25,
    PATCH_CUSTOMER_ID: 26,
    DELETE_CUSTOMER_ID: 27,
    POST_VENDOR_SIGNUP: 28,
    POST_VENDOR_LOGIN: 29,
    POST_VENDOR_LOGOUT: 30,
    GET_VENDOR_VERIFYEMAIL: 31,
    POST_VENDOR_CHANGEPASSWORD: 32,
    POST_VENDOR_FORGOTPASSWORD: 33,
    POST_VENDOR_RESETPASSWORD: 34,
    PATCH_VENDOR_ME: 35,
    GET_VENDOR_ME: 36,
    DELETE_VENDOR_ME: 37,
    GET_VENDOR: 38,
    GET_VENDOR_PUBLIC_ID: 39,
    POST_VENDOR_ID: 40,
    GET_VENDOR_ME_PRODUCT: 41,
    GET_VENDOR_ME_PRODUCT_ID: 42,
    PATCH_VENDOR_ME_PRODUCT_ID: 43,
    DELETE_VENDOR_ME_PRODUCT_ID: 44,
    GET_VENDOR_ME_MAINPRODUCT: 45,
    DELETE_VENDOR_ME_MAINPRODUCT_ID: 46,
    POST_VENDOR_ME_PRODUCT_NEW: 47,
    POST_VENDOR_ME_PRODUCT_EXISTING_ID: 48,
    GET_VENDOR_ME_PRODUCT_REQUEST: 49,
    GET_VENDOR_ME_PRODUCT_REQUEST_ID: 50,
    PATCH_VENDOR_ME_PRODUCT_REQUEST_ID: 51,
    DELETE_VENDOR_ME_PRODUCT_REQUEST_ID: 52,
    GET_COMMENT_ID_ALL: 53,
    GET_COMMENT_ID: 54,
    POST_COMMENT_ID: 55,
    PATCH_COMMENT_ID: 56,
    DELETE_COMMENT_ID: 57,
    GET_PRODUCT: 58,
    POST_PRODUCT: 59,
    GET_PRODUCT_ID: 60,
    POST_PRODUCT_ID: 61,
    PATCH_PRODUCT_ID: 62,
    DELETE_PRODUCT_ID: 63,
    PATCH_PRODUCT_ID_VENDOR_ID: 64,
    DELETE_PRODUCT_ID_VENDOR_ID: 65,
    POST_PRODUCT_SEARCH: 66,
    POST_PRODUCT_SEARCHFILTERS: 67,
    GET_MAINPRODUCT: 68,
    POST_MAINPRODUCT: 69,
    GET_MAINPRODUCT_ID: 70,
    PATCH_MAINPRODUCT_ID: 71,
    DELETE_MAINPRODUCT_ID: 72,
    DELETE_MAINPRODUCT_ID_VENDOR_ID: 73,
    GET_PRODUCTREQUEST: 74,
    GET_PRODUCTREQUEST_ID: 75,
    POST_PRODUCTREQUEST_ID: 76,
    DELETE_PRODUCTREQUEST_ID: 77,
    GET_TICKET: 78,
    POST_TICKET: 79,
    GET_TICKET_ID: 80,
    POST_TICKET_ID: 81,
    PATCH_TICKET_ID: 82,
    DELETE_TICKET_ID: 83,
    GET_TICKET_ALL: 84,
    GET_TICKET_ALL_UNASSIGNED: 85,
    GET_TICKET_ADMIN_ID: 86,
    GET_TICKET_ALL_ADMIN_ID: 87,
    GET_TICKET_CLIENT_ID: 88,
    GET_TICKET_ALL_CLIENT_ID: 89,
    GET_TICKET_ADMIN_ID_CLIENT_ID: 90,
    GET_TICKET_ALL_ADMIN_ID_CLIENT_ID: 91,
    GET_SHOPPINGLIST_WATCHLIST: 92,
    POST_SHOPPINGLIST_WATCHLIST: 93,
    DELETE_SHOPPINGLIST_WATCHLIST: 94,
    GET_CUSTOMER_NOTIFICATION: 95,
    POST_CUSTOMER_NOTIFICATION: 96,
    GET_VENDOR_NOTIFICATION: 97,
    POST_VENDOR_NOTIFICATION: 98,
  },
  TARGETS: {
    CATEGORY: {
      ONE: "One category.",
      MANY: "Many categories.",
    },
    SHOPPINGLIST: {
      ONE: "One shoppinglist.",
      MANY: "Many shoppinglists.",
    },
    CUSTOMER: {
      ONE: "One customer.",
      MANY: "Many customers",
    },
    VENDOR: {
      ONE: "One vendor.",
      MANY: "Many vendors.",
    },
    COMMENT: {
      ONE: "One comments.",
      MANY: "Many comments.",
    },
    PRODUCT: {
      ONE: "One product.",
      MANY: "Many products.",
    },
    MAINPRODUCT: {
      ONE: "One mainproducts.",
      MANY: "Many mainproducts.",
    },
    PRODUCTREQUEST: {
      ONE: "One mainproducts.",
      MANY: "Many mainproducts.",
    },
    TICKET: {
      ONE: "One ticket.",
      MANY: "Many tickets.",
    },
    NOTIFICATION: {
      ONE: "One notification.",
      MANY: "Many notifications.",
    },
  },
  NOTIFICATION_TYPES: {
    PRICE_DOWN_BELOW_THRESHOLD: "Product price is down below to its 90%.",
    PRICE_STRICTLY_DOWN_BELOW_THRESHOLD: "Product price is down below to its 75%.",
    PRICE_HOLY_DOWN_BELOW_THRESHOLD: "Product price is down below to its 50%.",
    AMOUNT_INCREASED: "Product amount has increased.",
    AMOUNT_GREATLY_INCREASED: "Product amount has greatly increased.",
    AMOUNT_HOLILY_INCREASED: "Product amount has holily increased.",
    PRODUCT_AMOUNT_BELOW_10: "Number of the specified product is below 10.",
    PRODUCT_AMOUNT_BELOW_5: "Number of the specified product is below 5.",
    TICKET_REPLIED_BY_ADMIN: "One of your tickets has been replied by an admin.",
    ORDER_MESSAGE_REPLIED_BY_VENDOR: "One of your order messages has been replied by a vendor.",
    ORDER_MESSAGE_REPLIED_BY_CUSTOMER: "One of your order messages has been replied by a customer.",
  },
  BASIC_COLORS: ["black", "blue", "red", "green", "orange", "violet", "white", "brown"],
};

module.exports = constants;