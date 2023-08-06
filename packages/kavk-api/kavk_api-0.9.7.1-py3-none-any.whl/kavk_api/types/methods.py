from typing import Optional
from .base import BaseMethod
from .objects import *
from .responses import *


class Account(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def ban(self, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.ban", **args)
		return BaseOkResponse(**r)


	async def changePassword(self, restore_sid:Optional[str]=None, change_password_hash:Optional[str]=None, old_password:Optional[str]=None, new_password:Optional[str]=None):
		"""Changes a user password after access is successfully restored with the [vk.com/dev/auth.restore|auth.restore] method."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.changePassword", **args)
		return AccountChangePasswordResponse(**r)


	async def getActiveOffers(self, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of active ads (offers) which executed by the user will bring him/her respective number of votes to his balance in the application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getActiveOffers", **args)
		return AccountGetActiveOffersResponse(**r)


	async def getAppPermissions(self, user_id:Optional[int]=None):
		"""Gets settings of the user in this application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getAppPermissions", **args)
		return AccountGetAppPermissionsResponse(**r)


	async def getBanned(self, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a user's blacklist."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getBanned", **args)
		return AccountGetBannedResponse(**r)


	async def getCounters(self, filter:Optional[list]=None, user_id:Optional[int]=None):
		"""Returns non-null values of user counters."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getCounters", **args)
		return AccountGetCountersResponse(**r)


	async def getInfo(self, fields:Optional[list]=None):
		"""Returns current account info."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getInfo", **args)
		return AccountGetInfoResponse(**r)


	async def getProfileInfo(self):
		"""Returns the current account info."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getProfileInfo", **args)
		return AccountGetProfileInfoResponse(**r)


	async def getPushSettings(self, device_id:Optional[str]=None):
		"""Gets settings of push notifications."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.getPushSettings", **args)
		return AccountGetPushSettingsResponse(**r)


	async def registerDevice(self, token:Optional[str]=None, device_model:Optional[str]=None, device_year:Optional[int]=None, device_id:Optional[str]=None, system_version:Optional[str]=None, settings:Optional[str]=None, sandbox:Optional[bool]=None):
		"""Subscribes an iOS/Android/Windows Phone-based device to receive push notifications"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.registerDevice", **args)
		return BaseOkResponse(**r)


	async def saveProfileInfo(self, first_name:Optional[str]=None, last_name:Optional[str]=None, maiden_name:Optional[str]=None, screen_name:Optional[str]=None, cancel_request_id:Optional[int]=None, sex:Optional[int]=None, relation:Optional[int]=None, relation_partner_id:Optional[int]=None, bdate:Optional[str]=None, bdate_visibility:Optional[int]=None, home_town:Optional[str]=None, country_id:Optional[int]=None, city_id:Optional[int]=None, status:Optional[str]=None):
		"""Edits current profile info."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.saveProfileInfo", **args)
		return AccountSaveProfileInfoResponse(**r)


	async def setInfo(self, name:Optional[str]=None, value:Optional[str]=None):
		"""Allows to edit the current account info."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.setInfo", **args)
		return BaseOkResponse(**r)


	async def setOffline(self):
		"""Marks a current user as offline."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.setOffline", **args)
		return BaseOkResponse(**r)


	async def setOnline(self, voip:Optional[bool]=None):
		"""Marks the current user as online for 15 minutes."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.setOnline", **args)
		return BaseOkResponse(**r)


	async def setPushSettings(self, device_id:Optional[str]=None, settings:Optional[str]=None, key:Optional[str]=None, value:Optional[list]=None):
		"""Change push settings."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.setPushSettings", **args)
		return BaseOkResponse(**r)


	async def setSilenceMode(self, device_id:Optional[str]=None, time:Optional[int]=None, peer_id:Optional[int]=None, sound:Optional[int]=None):
		"""Mutes push notifications for the set period of time."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.setSilenceMode", **args)
		return BaseOkResponse(**r)


	async def unban(self, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.unban", **args)
		return BaseOkResponse(**r)


	async def unregisterDevice(self, device_id:Optional[str]=None, sandbox:Optional[bool]=None):
		"""Unsubscribes a device from push notifications."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("account.unregisterDevice", **args)
		return BaseOkResponse(**r)



class Ads(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addOfficeUsers(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Adds managers and/or supervisors to advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.addOfficeUsers", **args)
		return AdsAddOfficeUsersResponse(**r)


	async def checkLink(self, account_id:Optional[int]=None, link_type:Optional[str]=None, link_url:Optional[str]=None, campaign_id:Optional[int]=None):
		"""Allows to check the ad link."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.checkLink", **args)
		return AdsCheckLinkResponse(**r)


	async def createAds(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Creates ads."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.createAds", **args)
		return AdsCreateAdsResponse.parse_obj(r)


	async def createCampaigns(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Creates advertising campaigns."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.createCampaigns", **args)
		return AdsCreateCampaignsResponse.parse_obj(r)


	async def createClients(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Creates clients of an advertising agency."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.createClients", **args)
		return AdsCreateClientsResponse.parse_obj(r)


	async def createTargetGroup(self, account_id:Optional[int]=None, client_id:Optional[int]=None, name:Optional[str]=None, lifetime:Optional[int]=None, target_pixel_id:Optional[int]=None, target_pixel_rules:Optional[str]=None):
		"""Creates a group to re-target ads for users who visited advertiser's site (viewed information about the product, registered, etc.)."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.createTargetGroup", **args)
		return AdsCreateTargetGroupResponse(**r)


	async def deleteAds(self, account_id:Optional[int]=None, ids:Optional[str]=None):
		"""Archives ads."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.deleteAds", **args)
		return AdsDeleteAdsResponse.parse_obj(r)


	async def deleteCampaigns(self, account_id:Optional[int]=None, ids:Optional[str]=None):
		"""Archives advertising campaigns."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.deleteCampaigns", **args)
		return AdsDeleteCampaignsResponse.parse_obj(r)


	async def deleteClients(self, account_id:Optional[int]=None, ids:Optional[str]=None):
		"""Archives clients of an advertising agency."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.deleteClients", **args)
		return AdsDeleteClientsResponse.parse_obj(r)


	async def deleteTargetGroup(self, account_id:Optional[int]=None, client_id:Optional[int]=None, target_group_id:Optional[int]=None):
		"""Deletes a retarget group."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.deleteTargetGroup", **args)
		return BaseOkResponse(**r)


	async def getAccounts(self):
		"""Returns a list of advertising accounts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getAccounts", **args)
		return AdsGetAccountsResponse.parse_obj(r)


	async def getAds(self, account_id:Optional[int]=None, ad_ids:Optional[str]=None, campaign_ids:Optional[str]=None, client_id:Optional[int]=None, include_deleted:Optional[bool]=None, only_deleted:Optional[bool]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		"""Returns number of ads."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getAds", **args)
		return AdsGetAdsResponse.parse_obj(r)


	async def getAdsLayout(self, account_id:Optional[int]=None, client_id:Optional[int]=None, include_deleted:Optional[bool]=None, only_deleted:Optional[bool]=None, campaign_ids:Optional[str]=None, ad_ids:Optional[str]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		"""Returns descriptions of ad layouts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getAdsLayout", **args)
		return AdsGetAdsLayoutResponse.parse_obj(r)


	async def getAdsTargeting(self, account_id:Optional[int]=None, ad_ids:Optional[str]=None, campaign_ids:Optional[str]=None, client_id:Optional[int]=None, include_deleted:Optional[bool]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		"""Returns ad targeting parameters."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getAdsTargeting", **args)
		return AdsGetAdsTargetingResponse.parse_obj(r)


	async def getBudget(self, account_id:Optional[int]=None):
		"""Returns current budget of the advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getBudget", **args)
		return AdsGetBudgetResponse(**r)


	async def getCampaigns(self, account_id:Optional[int]=None, client_id:Optional[int]=None, include_deleted:Optional[bool]=None, campaign_ids:Optional[str]=None, fields:Optional[list]=None):
		"""Returns a list of campaigns in an advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getCampaigns", **args)
		return AdsGetCampaignsResponse.parse_obj(r)


	async def getCategories(self, lang:Optional[str]=None):
		"""Returns a list of possible ad categories."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getCategories", **args)
		return AdsGetCategoriesResponse(**r)


	async def getClients(self, account_id:Optional[int]=None):
		"""Returns a list of advertising agency's clients."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getClients", **args)
		return AdsGetClientsResponse.parse_obj(r)


	async def getDemographics(self, account_id:Optional[int]=None, ids_type:Optional[str]=None, ids:Optional[str]=None, period:Optional[str]=None, date_from:Optional[str]=None, date_to:Optional[str]=None):
		"""Returns demographics for ads or campaigns."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getDemographics", **args)
		return AdsGetDemographicsResponse.parse_obj(r)


	async def getFloodStats(self, account_id:Optional[int]=None):
		"""Returns information about current state of a counter — number of remaining runs of methods and time to the next counter nulling in seconds."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getFloodStats", **args)
		return AdsGetFloodStatsResponse(**r)


	async def getLookalikeRequests(self, account_id:Optional[int]=None, client_id:Optional[int]=None, requests_ids:Optional[str]=None, offset:Optional[int]=None, limit:Optional[int]=None, sort_by:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getLookalikeRequests", **args)
		return AdsGetLookalikeRequestsResponse(**r)


	async def getMusicians(self, artist_name:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getMusicians", **args)
		return AdsGetMusiciansResponse(**r)


	async def getMusiciansByIds(self, ids:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getMusiciansByIds", **args)
		return AdsGetMusiciansResponse(**r)


	async def getOfficeUsers(self, account_id:Optional[int]=None):
		"""Returns a list of managers and supervisors of advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getOfficeUsers", **args)
		return AdsGetOfficeUsersResponse.parse_obj(r)


	async def getPostsReach(self, account_id:Optional[int]=None, ids_type:Optional[str]=None, ids:Optional[str]=None):
		"""Returns detailed statistics of promoted posts reach from campaigns and ads."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getPostsReach", **args)
		return AdsGetPostsReachResponse.parse_obj(r)


	async def getRejectionReason(self, account_id:Optional[int]=None, ad_id:Optional[int]=None):
		"""Returns a reason of ad rejection for pre-moderation."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getRejectionReason", **args)
		return AdsGetRejectionReasonResponse(**r)


	async def getStatistics(self, account_id:Optional[int]=None, ids_type:Optional[str]=None, ids:Optional[str]=None, period:Optional[str]=None, date_from:Optional[str]=None, date_to:Optional[str]=None, stats_fields:Optional[list]=None):
		"""Returns statistics of performance indicators for ads, campaigns, clients or the whole account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getStatistics", **args)
		return AdsGetStatisticsResponse.parse_obj(r)


	async def getSuggestions(self, section:Optional[str]=None, ids:Optional[str]=None, q:Optional[str]=None, country:Optional[int]=None, cities:Optional[str]=None, lang:Optional[str]=None):
		"""Returns a set of auto-suggestions for various targeting parameters."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getSuggestions", **args)
		for i in [AdsGetSuggestionsResponse, AdsGetSuggestionsRegionsResponse, AdsGetSuggestionsCitiesResponse, AdsGetSuggestionsSchoolsResponse]:
			try: return i(**r)
			except: return AdsGetSuggestionsResponse(**r)


	async def getTargetGroups(self, account_id:Optional[int]=None, client_id:Optional[int]=None, extended:Optional[bool]=None):
		"""Returns a list of target groups."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getTargetGroups", **args)
		return AdsGetTargetGroupsResponse.parse_obj(r)


	async def getTargetingStats(self, account_id:Optional[int]=None, client_id:Optional[int]=None, criteria:Optional[str]=None, ad_id:Optional[int]=None, ad_format:Optional[int]=None, ad_platform:Optional[str]=None, ad_platform_no_wall:Optional[str]=None, ad_platform_no_ad_network:Optional[str]=None, publisher_platforms:Optional[str]=None, link_url:Optional[str]=None, link_domain:Optional[str]=None, need_precise:Optional[bool]=None, impressions_limit_period:Optional[int]=None):
		"""Returns the size of targeting audience, and also recommended values for CPC and CPM."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getTargetingStats", **args)
		return AdsGetTargetingStatsResponse(**r)


	async def getUploadURL(self, ad_format:Optional[int]=None, icon:Optional[int]=None):
		"""Returns URL to upload an ad photo to."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getUploadURL", **args)
		return AdsGetUploadURLResponse(**r)


	async def getVideoUploadURL(self):
		"""Returns URL to upload an ad video to."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.getVideoUploadURL", **args)
		return AdsGetVideoUploadURLResponse(**r)


	async def importTargetContacts(self, account_id:Optional[int]=None, client_id:Optional[int]=None, target_group_id:Optional[int]=None, contacts:Optional[str]=None):
		"""Imports a list of advertiser's contacts to count VK registered users against the target group."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.importTargetContacts", **args)
		return AdsImportTargetContactsResponse(**r)


	async def removeOfficeUsers(self, account_id:Optional[int]=None, ids:Optional[str]=None):
		"""Removes managers and/or supervisors from advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.removeOfficeUsers", **args)
		return AdsRemoveOfficeUsersResponse(**r)


	async def updateAds(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Edits ads."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.updateAds", **args)
		return AdsUpdateAdsResponse.parse_obj(r)


	async def updateCampaigns(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Edits advertising campaigns."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.updateCampaigns", **args)
		return AdsUpdateCampaignsResponse(**r)


	async def updateClients(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Edits clients of an advertising agency."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.updateClients", **args)
		return AdsUpdateClientsResponse(**r)


	async def updateOfficeUsers(self, account_id:Optional[int]=None, data:Optional[str]=None):
		"""Adds managers and/or supervisors to advertising account."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.updateOfficeUsers", **args)
		return AdsUpdateOfficeUsersResponse.parse_obj(r)


	async def updateTargetGroup(self, account_id:Optional[int]=None, client_id:Optional[int]=None, target_group_id:Optional[int]=None, name:Optional[str]=None, domain:Optional[str]=None, lifetime:Optional[int]=None, target_pixel_id:Optional[int]=None, target_pixel_rules:Optional[str]=None):
		"""Edits a retarget group."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("ads.updateTargetGroup", **args)
		return BaseOkResponse(**r)



class Adsweb(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getAdCategories(self, office_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getAdCategories", **args)
		return AdswebGetAdCategoriesResponse(**r)


	async def getAdUnitCode(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getAdUnitCode", **args)
		return AdswebGetAdUnitCodeResponse(**r)


	async def getAdUnits(self, office_id:Optional[int]=None, sites_ids:Optional[str]=None, ad_units_ids:Optional[str]=None, fields:Optional[str]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getAdUnits", **args)
		return AdswebGetAdUnitsResponse(**r)


	async def getFraudHistory(self, office_id:Optional[int]=None, sites_ids:Optional[str]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getFraudHistory", **args)
		return AdswebGetFraudHistoryResponse(**r)


	async def getSites(self, office_id:Optional[int]=None, sites_ids:Optional[str]=None, fields:Optional[str]=None, limit:Optional[int]=None, offset:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getSites", **args)
		return AdswebGetSitesResponse(**r)


	async def getStatistics(self, office_id:Optional[int]=None, ids_type:Optional[str]=None, ids:Optional[str]=None, period:Optional[str]=None, date_from:Optional[str]=None, date_to:Optional[str]=None, fields:Optional[str]=None, limit:Optional[int]=None, page_id:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("adsweb.getStatistics", **args)
		return AdswebGetStatisticsResponse(**r)



class Appwidgets(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getAppImageUploadServer(self, image_type:Optional[str]=None):
		"""Returns a URL for uploading a photo to the community collection for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.getAppImageUploadServer", **args)
		return AppWidgetsGetAppImageUploadServerResponse(**r)


	async def getAppImages(self, offset:Optional[int]=None, count:Optional[int]=None, image_type:Optional[str]=None):
		"""Returns an app collection of images for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.getAppImages", **args)
		return AppWidgetsGetAppImagesResponse(**r)


	async def getGroupImageUploadServer(self, image_type:Optional[str]=None):
		"""Returns a URL for uploading a photo to the community collection for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.getGroupImageUploadServer", **args)
		return AppWidgetsGetGroupImageUploadServerResponse(**r)


	async def getGroupImages(self, offset:Optional[int]=None, count:Optional[int]=None, image_type:Optional[str]=None):
		"""Returns a community collection of images for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.getGroupImages", **args)
		return AppWidgetsGetGroupImagesResponse(**r)


	async def getImagesById(self, images:Optional[list]=None):
		"""Returns an image for community app widgets by its ID"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.getImagesById", **args)
		return AppWidgetsGetImagesByIdResponse.parse_obj(r)


	async def saveAppImage(self, hash:Optional[str]=None, image:Optional[str]=None):
		"""Allows to save image into app collection for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.saveAppImage", **args)
		return AppWidgetsSaveAppImageResponse(**r)


	async def saveGroupImage(self, hash:Optional[str]=None, image:Optional[str]=None):
		"""Allows to save image into community collection for community app widgets"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.saveGroupImage", **args)
		return AppWidgetsSaveGroupImageResponse(**r)


	async def update(self, code:Optional[str]=None, type:Optional[str]=None):
		"""Allows to update community app widget"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("appwidgets.update", **args)
		return BaseOkResponse(**r)



class Apps(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def deleteAppRequests(self):
		"""Deletes all request notifications from the current app."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.deleteAppRequests", **args)
		return BaseOkResponse(**r)


	async def get(self, app_id:Optional[int]=None, app_ids:Optional[list]=None, platform:Optional[str]=None, extended:Optional[bool]=None, return_friends:Optional[bool]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns applications data."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.get", **args)
		return AppsGetResponse(**r)


	async def getCatalog(self, sort:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None, platform:Optional[str]=None, extended:Optional[bool]=None, return_friends:Optional[bool]=None, fields:Optional[list]=None, name_case:Optional[str]=None, q:Optional[str]=None, genre_id:Optional[int]=None, filter:Optional[str]=None):
		"""Returns a list of applications (apps) available to users in the App Catalog."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getCatalog", **args)
		return AppsGetCatalogResponse(**r)


	async def getFriendsList(self, extended:Optional[bool]=None, count:Optional[int]=None, offset:Optional[int]=None, type:Optional[str]=None, fields:Optional[list]=None):
		"""Creates friends list for requests and invites in current app."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getFriendsList", **args)
		for i in [AppsGetFriendsListResponse, AppsGetFriendsListExtendedResponse]:
			try: return i(**r)
			except: return AppsGetFriendsListResponse(**r)


	async def getLeaderboard(self, type:Optional[str]=None, _global:Optional[bool]=None, extended:Optional[bool]=None):
		"""Returns players rating in the game."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getLeaderboard", **args)
		for i in [AppsGetLeaderboardResponse, AppsGetLeaderboardExtendedResponse]:
			try: return i(**r)
			except: return AppsGetLeaderboardResponse(**r)


	async def getMiniAppPolicies(self, app_id:Optional[int]=None):
		"""Returns policies and terms given to a mini app."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getMiniAppPolicies", **args)
		return AppsGetMiniAppPoliciesResponse(**r)


	async def getScopes(self, type:Optional[str]=None):
		"""Returns scopes for auth"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getScopes", **args)
		return AppsGetScopesResponse(**r)


	async def getScore(self, user_id:Optional[int]=None):
		"""Returns user score in app"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.getScore", **args)
		return AppsGetScoreResponse(**r)


	async def promoHasActiveGift(self, promo_id:Optional[int]=None, user_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.promoHasActiveGift", **args)
		return BaseBoolResponse(**r)


	async def promoUseGift(self, promo_id:Optional[int]=None, user_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.promoUseGift", **args)
		return BaseBoolResponse(**r)


	async def sendRequest(self, user_id:Optional[int]=None, text:Optional[str]=None, type:Optional[str]=None, name:Optional[str]=None, key:Optional[str]=None, separate:Optional[bool]=None):
		"""Sends a request to another user in an app that uses VK authorization."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("apps.sendRequest", **args)
		return AppsSendRequestResponse(**r)



class Auth(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def restore(self, phone:Optional[str]=None, last_name:Optional[str]=None):
		"""Allows to restore account access using a code received via SMS. ' This method is only available for apps with [vk.com/dev/auth_direct|Direct authorization] access. '"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("auth.restore", **args)
		return AuthRestoreResponse(**r)



class Board(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addTopic(self, group_id:Optional[int]=None, title:Optional[str]=None, text:Optional[str]=None, from_group:Optional[bool]=None, attachments:Optional[list]=None):
		"""Creates a new topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.addTopic", **args)
		return BoardAddTopicResponse(**r)


	async def closeTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None):
		"""Closes a topic on a community's discussion board so that comments cannot be posted."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.closeTopic", **args)
		return BaseOkResponse(**r)


	async def createComment(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, from_group:Optional[bool]=None, sticker_id:Optional[int]=None, guid:Optional[str]=None):
		"""Adds a comment on a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.createComment", **args)
		return BoardCreateCommentResponse(**r)


	async def deleteComment(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Deletes a comment on a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.deleteComment", **args)
		return BaseOkResponse(**r)


	async def deleteTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None):
		"""Deletes a topic from a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.deleteTopic", **args)
		return BaseOkResponse(**r)


	async def editComment(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, comment_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None):
		"""Edits a comment on a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.editComment", **args)
		return BaseOkResponse(**r)


	async def editTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, title:Optional[str]=None):
		"""Edits the title of a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.editTopic", **args)
		return BaseOkResponse(**r)


	async def fixTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None):
		"""Pins a topic (fixes its place) to the top of a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.fixTopic", **args)
		return BaseOkResponse(**r)


	async def getComments(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, need_likes:Optional[bool]=None, start_comment_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, sort:Optional[str]=None):
		"""Returns a list of comments on a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.getComments", **args)
		for i in [BoardGetCommentsResponse, BoardGetCommentsExtendedResponse]:
			try: return i(**r)
			except: return BoardGetCommentsResponse(**r)


	async def getTopics(self, group_id:Optional[int]=None, topic_ids:Optional[list]=None, order:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, preview:Optional[int]=None, preview_length:Optional[int]=None):
		"""Returns a list of topics on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.getTopics", **args)
		for i in [BoardGetTopicsResponse, BoardGetTopicsExtendedResponse]:
			try: return i(**r)
			except: return BoardGetTopicsResponse(**r)


	async def openTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None):
		"""Re-opens a previously closed topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.openTopic", **args)
		return BaseOkResponse(**r)


	async def restoreComment(self, group_id:Optional[int]=None, topic_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Restores a comment deleted from a topic on a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.restoreComment", **args)
		return BaseOkResponse(**r)


	async def unfixTopic(self, group_id:Optional[int]=None, topic_id:Optional[int]=None):
		"""Unpins a pinned topic from the top of a community's discussion board."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("board.unfixTopic", **args)
		return BaseOkResponse(**r)



class Database(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getChairs(self, faculty_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns list of chairs on a specified faculty."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getChairs", **args)
		return DatabaseGetChairsResponse(**r)


	async def getCities(self, country_id:Optional[int]=None, region_id:Optional[int]=None, q:Optional[str]=None, need_all:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of cities."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getCities", **args)
		return DatabaseGetCitiesResponse(**r)


	async def getCitiesById(self, city_ids:Optional[list]=None):
		"""Returns information about cities by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getCitiesById", **args)
		return DatabaseGetCitiesByIdResponse.parse_obj(r)


	async def getCountries(self, need_all:Optional[bool]=None, code:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of countries."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getCountries", **args)
		return DatabaseGetCountriesResponse(**r)


	async def getCountriesById(self, country_ids:Optional[list]=None):
		"""Returns information about countries by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getCountriesById", **args)
		return DatabaseGetCountriesByIdResponse.parse_obj(r)


	async def getFaculties(self, university_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of faculties (i.e., university departments)."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getFaculties", **args)
		return DatabaseGetFacultiesResponse(**r)


	async def getMetroStations(self, city_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None):
		"""Get metro stations by city"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getMetroStations", **args)
		return DatabaseGetMetroStationsResponse(**r)


	async def getMetroStationsById(self, station_ids:Optional[list]=None):
		"""Get metro station by his id"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getMetroStationsById", **args)
		return DatabaseGetMetroStationsByIdResponse.parse_obj(r)


	async def getRegions(self, country_id:Optional[int]=None, q:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of regions."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getRegions", **args)
		return DatabaseGetRegionsResponse(**r)


	async def getSchoolClasses(self, country_id:Optional[int]=None):
		"""Returns a list of school classes specified for the country."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getSchoolClasses", **args)
		return DatabaseGetSchoolClassesResponse.parse_obj(r)


	async def getSchools(self, q:Optional[str]=None, city_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of schools."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getSchools", **args)
		return DatabaseGetSchoolsResponse(**r)


	async def getUniversities(self, q:Optional[str]=None, country_id:Optional[int]=None, city_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of higher education institutions."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("database.getUniversities", **args)
		return DatabaseGetUniversitiesResponse(**r)



class Docs(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, owner_id:Optional[int]=None, doc_id:Optional[int]=None, access_key:Optional[str]=None):
		"""Copies a document to a user's or community's document list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.add", **args)
		return DocsAddResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, doc_id:Optional[int]=None):
		"""Deletes a user or community document."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.delete", **args)
		return BaseOkResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, doc_id:Optional[int]=None, title:Optional[str]=None, tags:Optional[list]=None):
		"""Edits a document."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.edit", **args)
		return BaseOkResponse(**r)


	async def get(self, count:Optional[int]=None, offset:Optional[int]=None, type:Optional[int]=None, owner_id:Optional[int]=None, return_tags:Optional[bool]=None):
		"""Returns detailed information about user or community documents."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.get", **args)
		return DocsGetResponse(**r)


	async def getById(self, docs:Optional[list]=None, return_tags:Optional[bool]=None):
		"""Returns information about documents by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.getById", **args)
		return DocsGetByIdResponse.parse_obj(r)


	async def getMessagesUploadServer(self, type:Optional[str]=None, peer_id:Optional[int]=None):
		"""Returns the server address for document upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.getMessagesUploadServer", **args)
		return DocsGetUploadServerResponse(**r)


	async def getTypes(self, owner_id:Optional[int]=None):
		"""Returns documents types available for current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.getTypes", **args)
		return DocsGetTypesResponse(**r)


	async def getUploadServer(self, group_id:Optional[int]=None):
		"""Returns the server address for document upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.getUploadServer", **args)
		return DocsGetUploadServerResponse(**r)


	async def getWallUploadServer(self, group_id:Optional[int]=None):
		"""Returns the server address for document upload onto a user's or community's wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.getWallUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def save(self, file:Optional[str]=None, title:Optional[str]=None, tags:Optional[str]=None, return_tags:Optional[bool]=None):
		"""Saves a document after [vk.com/dev/upload_files_2|uploading it to a server]."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.save", **args)
		return DocsSaveResponse(**r)


	async def search(self, q:Optional[str]=None, search_own:Optional[bool]=None, count:Optional[int]=None, offset:Optional[int]=None, return_tags:Optional[bool]=None):
		"""Returns a list of documents matching the search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("docs.search", **args)
		return DocsSearchResponse(**r)



class Donut(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getFriends(self, owner_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("donut.getFriends", **args)
		return GroupsGetMembersFieldsResponse(**r)


	async def getSubscription(self, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("donut.getSubscription", **args)
		return DonutGetSubscriptionResponse(**r)


	async def getSubscriptions(self, fields:Optional[list]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of user's VK Donut subscriptions."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("donut.getSubscriptions", **args)
		return DonutGetSubscriptionsResponse(**r)


	async def isDon(self, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("donut.isDon", **args)
		return BaseBoolResponse(**r)



class Downloadedgames(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getPaidStatus(self, user_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("downloadedgames.getPaidStatus", **args)
		return DownloadedGamesPaidStatusResponse(**r)



class Fave(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addArticle(self, url:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addArticle", **args)
		return BaseOkResponse(**r)


	async def addLink(self, link:Optional[str]=None):
		"""Adds a link to user faves."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addLink", **args)
		return BaseOkResponse(**r)


	async def addPage(self, user_id:Optional[int]=None, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addPage", **args)
		return BaseOkResponse(**r)


	async def addPost(self, owner_id:Optional[int]=None, id:Optional[int]=None, access_key:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addPost", **args)
		return BaseOkResponse(**r)


	async def addProduct(self, owner_id:Optional[int]=None, id:Optional[int]=None, access_key:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addProduct", **args)
		return BaseOkResponse(**r)


	async def addTag(self, name:Optional[str]=None, position:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addTag", **args)
		return FaveAddTagResponse(**r)


	async def addVideo(self, owner_id:Optional[int]=None, id:Optional[int]=None, access_key:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.addVideo", **args)
		return BaseOkResponse(**r)


	async def editTag(self, id:Optional[int]=None, name:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.editTag", **args)
		return BaseOkResponse(**r)


	async def get(self, extended:Optional[bool]=None, item_type:Optional[str]=None, tag_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[str]=None, is_from_snackbar:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.get", **args)
		for i in [FaveGetResponse, FaveGetExtendedResponse]:
			try: return i(**r)
			except: return FaveGetResponse(**r)


	async def getPages(self, offset:Optional[int]=None, count:Optional[int]=None, type:Optional[str]=None, fields:Optional[list]=None, tag_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.getPages", **args)
		return FaveGetPagesResponse(**r)


	async def getTags(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.getTags", **args)
		return FaveGetTagsResponse(**r)


	async def markSeen(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.markSeen", **args)
		return BaseBoolResponse(**r)


	async def removeArticle(self, owner_id:Optional[int]=None, article_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removeArticle", **args)
		return BaseBoolResponse(**r)


	async def removeLink(self, link_id:Optional[str]=None, link:Optional[str]=None):
		"""Removes link from the user's faves."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removeLink", **args)
		return BaseOkResponse(**r)


	async def removePage(self, user_id:Optional[int]=None, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removePage", **args)
		return BaseOkResponse(**r)


	async def removePost(self, owner_id:Optional[int]=None, id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removePost", **args)
		return BaseOkResponse(**r)


	async def removeProduct(self, owner_id:Optional[int]=None, id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removeProduct", **args)
		return BaseOkResponse(**r)


	async def removeTag(self, id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removeTag", **args)
		return BaseOkResponse(**r)


	async def removeVideo(self, owner_id:Optional[int]=None, id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.removeVideo", **args)
		return BaseOkResponse(**r)


	async def reorderTags(self, ids:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.reorderTags", **args)
		return BaseOkResponse(**r)


	async def setPageTags(self, user_id:Optional[int]=None, group_id:Optional[int]=None, tag_ids:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.setPageTags", **args)
		return BaseOkResponse(**r)


	async def setTags(self, item_type:Optional[str]=None, item_owner_id:Optional[int]=None, item_id:Optional[int]=None, tag_ids:Optional[list]=None, link_id:Optional[str]=None, link_url:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.setTags", **args)
		return BaseOkResponse(**r)


	async def trackPageInteraction(self, user_id:Optional[int]=None, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("fave.trackPageInteraction", **args)
		return BaseOkResponse(**r)



class Friends(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, user_id:Optional[int]=None, text:Optional[str]=None, follow:Optional[bool]=None):
		"""Approves or creates a friend request."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.add", **args)
		return FriendsAddResponse(**r)


	async def addList(self, name:Optional[str]=None, user_ids:Optional[list]=None):
		"""Creates a new friend list for the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.addList", **args)
		return FriendsAddListResponse(**r)


	async def areFriends(self, user_ids:Optional[list]=None, need_sign:Optional[bool]=None, extended:Optional[bool]=None):
		"""Checks the current user's friendship status with other specified users."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.areFriends", **args)
		for i in [FriendsAreFriendsResponse, FriendsAreFriendsExtendedResponse]:
			try: return i(**r)
			except: return FriendsAreFriendsResponse(**r)


	async def delete(self, user_id:Optional[int]=None):
		"""Declines a friend request or deletes a user from the current user's friend list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.delete", **args)
		return FriendsDeleteResponse(**r)


	async def deleteAllRequests(self):
		"""Marks all incoming friend requests as viewed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.deleteAllRequests", **args)
		return BaseOkResponse(**r)


	async def deleteList(self, list_id:Optional[int]=None):
		"""Deletes a friend list of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.deleteList", **args)
		return BaseOkResponse(**r)


	async def edit(self, user_id:Optional[int]=None, list_ids:Optional[list]=None):
		"""Edits the friend lists of the selected user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.edit", **args)
		return BaseOkResponse(**r)


	async def editList(self, name:Optional[str]=None, list_id:Optional[int]=None, user_ids:Optional[list]=None, add_user_ids:Optional[list]=None, delete_user_ids:Optional[list]=None):
		"""Edits a friend list of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.editList", **args)
		return BaseOkResponse(**r)


	async def get(self, user_id:Optional[int]=None, order:Optional[str]=None, list_id:Optional[int]=None, count:Optional[int]=None, offset:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None, ref:Optional[str]=None):
		"""Returns a list of user IDs or detailed information about a user's friends."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.get", **args)
		for i in [FriendsGetResponse, FriendsGetFieldsResponse]:
			try: return i(**r)
			except: return FriendsGetResponse(**r)


	async def getAppUsers(self):
		"""Returns a list of IDs of the current user's friends who installed the application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getAppUsers", **args)
		return FriendsGetAppUsersResponse.parse_obj(r)


	async def getByPhones(self, phones:Optional[list]=None, fields:Optional[list]=None):
		"""Returns a list of the current user's friends whose phone numbers, validated or specified in a profile, are in a given list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getByPhones", **args)
		return FriendsGetByPhonesResponse.parse_obj(r)


	async def getLists(self, user_id:Optional[int]=None, return_system:Optional[bool]=None):
		"""Returns a list of the user's friend lists."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getLists", **args)
		return FriendsGetListsResponse(**r)


	async def getMutual(self, source_uid:Optional[int]=None, target_uid:Optional[int]=None, target_uids:Optional[list]=None, order:Optional[str]=None, count:Optional[int]=None, offset:Optional[int]=None):
		"""Returns a list of user IDs of the mutual friends of two users."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getMutual", **args)
		for i in [FriendsGetMutualResponse, FriendsGetMutualTargetUidsResponse]:
			try: return i(**r)
			except: return FriendsGetMutualResponse(**r)


	async def getOnline(self, user_id:Optional[int]=None, list_id:Optional[int]=None, online_mobile:Optional[bool]=None, order:Optional[str]=None, count:Optional[int]=None, offset:Optional[int]=None):
		"""Returns a list of user IDs of a user's friends who are online."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getOnline", **args)
		for i in [FriendsGetOnlineResponse, FriendsGetOnlineOnlineMobileResponse]:
			try: return i(**r)
			except: return FriendsGetOnlineResponse(**r)


	async def getRecent(self, count:Optional[int]=None):
		"""Returns a list of user IDs of the current user's recently added friends."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getRecent", **args)
		return FriendsGetRecentResponse.parse_obj(r)


	async def getRequests(self, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, need_mutual:Optional[bool]=None, out:Optional[bool]=None, sort:Optional[int]=None, need_viewed:Optional[bool]=None, suggested:Optional[bool]=None, ref:Optional[str]=None, fields:Optional[list]=None):
		"""Returns information about the current user's incoming and outgoing friend requests."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getRequests", **args)
		for i in [FriendsGetRequestsResponse, FriendsGetRequestsNeedMutualResponse, FriendsGetRequestsExtendedResponse]:
			try: return i(**r)
			except: return FriendsGetRequestsResponse(**r)


	async def getSuggestions(self, filter:Optional[list]=None, count:Optional[int]=None, offset:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns a list of profiles of users whom the current user may know."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.getSuggestions", **args)
		return FriendsGetSuggestionsResponse(**r)


	async def search(self, user_id:Optional[int]=None, q:Optional[str]=None, fields:Optional[list]=None, name_case:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of friends matching the search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("friends.search", **args)
		return FriendsSearchResponse(**r)



class Gifts(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, user_id:Optional[int]=None, count:Optional[int]=None, offset:Optional[int]=None):
		"""Returns a list of user gifts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("gifts.get", **args)
		return GiftsGetResponse(**r)



class Groups(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addAddress(self, group_id:Optional[int]=None, title:Optional[str]=None, address:Optional[str]=None, additional_address:Optional[str]=None, country_id:Optional[int]=None, city_id:Optional[int]=None, metro_id:Optional[int]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, phone:Optional[str]=None, work_info_status:Optional[str]=None, timetable:Optional[str]=None, is_main_address:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.addAddress", **args)
		return GroupsAddAddressResponse(**r)


	async def addCallbackServer(self, group_id:Optional[int]=None, url:Optional[str]=None, title:Optional[str]=None, secret_key:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.addCallbackServer", **args)
		return GroupsAddCallbackServerResponse(**r)


	async def addLink(self, group_id:Optional[int]=None, link:Optional[str]=None, text:Optional[str]=None):
		"""Allows to add a link to the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.addLink", **args)
		return GroupsAddLinkResponse(**r)


	async def approveRequest(self, group_id:Optional[int]=None, user_id:Optional[int]=None):
		"""Allows to approve join request to the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.approveRequest", **args)
		return BaseOkResponse(**r)


	async def ban(self, group_id:Optional[int]=None, owner_id:Optional[int]=None, end_date:Optional[int]=None, reason:Optional[int]=None, comment:Optional[str]=None, comment_visible:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.ban", **args)
		return BaseOkResponse(**r)


	async def create(self, title:Optional[str]=None, description:Optional[str]=None, type:Optional[str]=None, public_category:Optional[int]=None, public_subcategory:Optional[int]=None, subtype:Optional[int]=None):
		"""Creates a new community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.create", **args)
		return GroupsCreateResponse(**r)


	async def deleteAddress(self, group_id:Optional[int]=None, address_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.deleteAddress", **args)
		return BaseOkResponse(**r)


	async def deleteCallbackServer(self, group_id:Optional[int]=None, server_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.deleteCallbackServer", **args)
		return BaseOkResponse(**r)


	async def deleteLink(self, group_id:Optional[int]=None, link_id:Optional[int]=None):
		"""Allows to delete a link from the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.deleteLink", **args)
		return BaseOkResponse(**r)


	async def disableOnline(self, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.disableOnline", **args)
		return BaseOkResponse(**r)


	async def edit(self, group_id:Optional[int]=None, title:Optional[str]=None, description:Optional[str]=None, screen_name:Optional[str]=None, access:Optional[int]=None, website:Optional[str]=None, subject:Optional[str]=None, email:Optional[str]=None, phone:Optional[str]=None, rss:Optional[str]=None, event_start_date:Optional[int]=None, event_finish_date:Optional[int]=None, event_group_id:Optional[int]=None, public_category:Optional[int]=None, public_subcategory:Optional[int]=None, public_date:Optional[str]=None, wall:Optional[int]=None, topics:Optional[int]=None, photos:Optional[int]=None, video:Optional[int]=None, audio:Optional[int]=None, links:Optional[bool]=None, events:Optional[bool]=None, places:Optional[bool]=None, contacts:Optional[bool]=None, docs:Optional[int]=None, wiki:Optional[int]=None, messages:Optional[bool]=None, articles:Optional[bool]=None, addresses:Optional[bool]=None, age_limits:Optional[int]=None, market:Optional[bool]=None, market_comments:Optional[bool]=None, market_country:Optional[list]=None, market_city:Optional[list]=None, market_currency:Optional[int]=None, market_contact:Optional[int]=None, market_wiki:Optional[int]=None, obscene_filter:Optional[bool]=None, obscene_stopwords:Optional[bool]=None, obscene_words:Optional[list]=None, main_section:Optional[int]=None, secondary_section:Optional[int]=None, country:Optional[int]=None, city:Optional[int]=None):
		"""Edits a community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.edit", **args)
		return BaseOkResponse(**r)


	async def editAddress(self, group_id:Optional[int]=None, address_id:Optional[int]=None, title:Optional[str]=None, address:Optional[str]=None, additional_address:Optional[str]=None, country_id:Optional[int]=None, city_id:Optional[int]=None, metro_id:Optional[int]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, phone:Optional[str]=None, work_info_status:Optional[str]=None, timetable:Optional[str]=None, is_main_address:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.editAddress", **args)
		return GroupsEditAddressResponse(**r)


	async def editCallbackServer(self, group_id:Optional[int]=None, server_id:Optional[int]=None, url:Optional[str]=None, title:Optional[str]=None, secret_key:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.editCallbackServer", **args)
		return BaseOkResponse(**r)


	async def editLink(self, group_id:Optional[int]=None, link_id:Optional[int]=None, text:Optional[str]=None):
		"""Allows to edit a link in the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.editLink", **args)
		return BaseOkResponse(**r)


	async def editManager(self, group_id:Optional[int]=None, user_id:Optional[int]=None, role:Optional[str]=None, is_contact:Optional[bool]=None, contact_position:Optional[str]=None, contact_phone:Optional[str]=None, contact_email:Optional[str]=None):
		"""Allows to add, remove or edit the community manager."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.editManager", **args)
		return BaseOkResponse(**r)


	async def enableOnline(self, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.enableOnline", **args)
		return BaseOkResponse(**r)


	async def get(self, user_id:Optional[int]=None, extended:Optional[bool]=None, filter:Optional[list]=None, fields:Optional[list]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of the communities to which a user belongs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.get", **args)
		for i in [GroupsGetResponse, GroupsGetObjectExtendedResponse]:
			try: return i(**r)
			except: return GroupsGetResponse(**r)


	async def getAddresses(self, group_id:Optional[int]=None, address_ids:Optional[list]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None):
		"""Returns a list of community addresses."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getAddresses", **args)
		return GroupsGetAddressesResponse(**r)


	async def getBanned(self, group_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, owner_id:Optional[int]=None):
		"""Returns a list of users on a community blacklist."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getBanned", **args)
		return GroupsGetBannedResponse(**r)


	async def getById(self, group_ids:Optional[list]=None, group_id:Optional[list[int|str]]=None, fields:Optional[list]=None):
		"""Returns information about communities by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getById", **args)
		return GroupsGetByIdObjectLegacyResponse.parse_obj(r)


	async def getCallbackConfirmationCode(self, group_id:Optional[int]=None):
		"""Returns Callback API confirmation code for the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getCallbackConfirmationCode", **args)
		return GroupsGetCallbackConfirmationCodeResponse(**r)


	async def getCallbackServers(self, group_id:Optional[int]=None, server_ids:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getCallbackServers", **args)
		return GroupsGetCallbackServersResponse(**r)


	async def getCallbackSettings(self, group_id:Optional[int]=None, server_id:Optional[int]=None):
		"""Returns [vk.com/dev/callback_api|Callback API] notifications settings."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getCallbackSettings", **args)
		return GroupsGetCallbackSettingsResponse(**r)


	async def getCatalog(self, category_id:Optional[int]=None, subcategory_id:Optional[int]=None):
		"""Returns communities list for a catalog category."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getCatalog", **args)
		return GroupsGetCatalogResponse(**r)


	async def getCatalogInfo(self, extended:Optional[bool]=None, subcategories:Optional[bool]=None):
		"""Returns categories list for communities catalog"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getCatalogInfo", **args)
		for i in [GroupsGetCatalogInfoResponse, GroupsGetCatalogInfoExtendedResponse]:
			try: return i(**r)
			except: return GroupsGetCatalogInfoResponse(**r)


	async def getInvitedUsers(self, group_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns invited users list of a community"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getInvitedUsers", **args)
		return GroupsGetInvitedUsersResponse(**r)


	async def getInvites(self, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None):
		"""Returns a list of invitations to join communities and events."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getInvites", **args)
		for i in [GroupsGetInvitesResponse, GroupsGetInvitesExtendedResponse]:
			try: return i(**r)
			except: return GroupsGetInvitesResponse(**r)


	async def getLongPollServer(self, group_id:Optional[int]=None):
		"""Returns the data needed to query a Long Poll server for events"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getLongPollServer", **args)
		return GroupsGetLongPollServerResponse(**r)


	async def getLongPollSettings(self, group_id:Optional[int]=None):
		"""Returns Long Poll notification settings"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getLongPollSettings", **args)
		return GroupsGetLongPollSettingsResponse(**r)


	async def getMembers(self, group_id:Optional[str]=None, sort:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, filter:Optional[str]=None):
		"""Returns a list of community members."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getMembers", **args)
		for i in [GroupsGetMembersResponse, GroupsGetMembersFieldsResponse, GroupsGetMembersFilterResponse]:
			try: return i(**r)
			except: return GroupsGetMembersResponse(**r)


	async def getRequests(self, group_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None):
		"""Returns a list of requests to the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getRequests", **args)
		for i in [GroupsGetRequestsResponse, GroupsGetRequestsFieldsResponse]:
			try: return i(**r)
			except: return GroupsGetRequestsResponse(**r)


	async def getSettings(self, group_id:Optional[int]=None):
		"""Returns community settings."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getSettings", **args)
		return GroupsGetSettingsResponse(**r)


	async def getTagList(self, group_id:Optional[int]=None):
		"""List of group's tags"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getTagList", **args)
		return GroupsGetTagListResponse.parse_obj(r)


	async def getTokenPermissions(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.getTokenPermissions", **args)
		return GroupsGetTokenPermissionsResponse(**r)


	async def invite(self, group_id:Optional[int]=None, user_id:Optional[int]=None):
		"""Allows to invite friends to the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.invite", **args)
		return BaseOkResponse(**r)


	async def isMember(self, group_id:Optional[str]=None, user_id:Optional[int]=None, user_ids:Optional[list]=None, extended:Optional[bool]=None):
		"""Returns information specifying whether a user is a member of a community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.isMember", **args)
		for i in [GroupsIsMemberResponse, GroupsIsMemberUserIdsResponse, GroupsIsMemberExtendedResponse, GroupsIsMemberUserIdsExtendedResponse]:
			try: return i(**r)
			except: return GroupsIsMemberResponse(**r)


	async def join(self, group_id:Optional[int]=None, not_sure:Optional[str]=None):
		"""With this method you can join the group or public page, and also confirm your participation in an event."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.join", **args)
		return BaseOkResponse(**r)


	async def leave(self, group_id:Optional[int]=None):
		"""With this method you can leave a group, public page, or event."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.leave", **args)
		return BaseOkResponse(**r)


	async def removeUser(self, group_id:Optional[int]=None, user_id:Optional[int]=None):
		"""Removes a user from the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.removeUser", **args)
		return BaseOkResponse(**r)


	async def reorderLink(self, group_id:Optional[int]=None, link_id:Optional[int]=None, after:Optional[int]=None):
		"""Allows to reorder links in the community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.reorderLink", **args)
		return BaseOkResponse(**r)


	async def search(self, q:Optional[str]=None, type:Optional[str]=None, country_id:Optional[int]=None, city_id:Optional[int]=None, future:Optional[bool]=None, market:Optional[bool]=None, sort:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of communities matching the search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.search", **args)
		return GroupsSearchResponse(**r)


	async def setCallbackSettings(self, group_id:Optional[int]=None, server_id:Optional[int]=None, api_version:Optional[str]=None, message_new:Optional[bool]=None, message_reply:Optional[bool]=None, message_allow:Optional[bool]=None, message_edit:Optional[bool]=None, message_deny:Optional[bool]=None, message_typing_state:Optional[bool]=None, photo_new:Optional[bool]=None, audio_new:Optional[bool]=None, video_new:Optional[bool]=None, wall_reply_new:Optional[bool]=None, wall_reply_edit:Optional[bool]=None, wall_reply_delete:Optional[bool]=None, wall_reply_restore:Optional[bool]=None, wall_post_new:Optional[bool]=None, wall_repost:Optional[bool]=None, board_post_new:Optional[bool]=None, board_post_edit:Optional[bool]=None, board_post_restore:Optional[bool]=None, board_post_delete:Optional[bool]=None, photo_comment_new:Optional[bool]=None, photo_comment_edit:Optional[bool]=None, photo_comment_delete:Optional[bool]=None, photo_comment_restore:Optional[bool]=None, video_comment_new:Optional[bool]=None, video_comment_edit:Optional[bool]=None, video_comment_delete:Optional[bool]=None, video_comment_restore:Optional[bool]=None, market_comment_new:Optional[bool]=None, market_comment_edit:Optional[bool]=None, market_comment_delete:Optional[bool]=None, market_comment_restore:Optional[bool]=None, market_order_new:Optional[bool]=None, market_order_edit:Optional[bool]=None, poll_vote_new:Optional[bool]=None, group_join:Optional[bool]=None, group_leave:Optional[bool]=None, group_change_settings:Optional[bool]=None, group_change_photo:Optional[bool]=None, group_officers_edit:Optional[bool]=None, user_block:Optional[bool]=None, user_unblock:Optional[bool]=None, lead_forms_new:Optional[bool]=None, like_add:Optional[bool]=None, like_remove:Optional[bool]=None, message_event:Optional[bool]=None, donut_subscription_create:Optional[bool]=None, donut_subscription_prolonged:Optional[bool]=None, donut_subscription_cancelled:Optional[bool]=None, donut_subscription_price_changed:Optional[bool]=None, donut_subscription_expired:Optional[bool]=None, donut_money_withdraw:Optional[bool]=None, donut_money_withdraw_error:Optional[bool]=None):
		"""Allow to set notifications settings for group."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.setCallbackSettings", **args)
		return BaseOkResponse(**r)


	async def setLongPollSettings(self, group_id:Optional[int]=None, enabled:Optional[bool]=None, api_version:Optional[str]=None, message_new:Optional[bool]=None, message_reply:Optional[bool]=None, message_allow:Optional[bool]=None, message_deny:Optional[bool]=None, message_edit:Optional[bool]=None, message_typing_state:Optional[bool]=None, photo_new:Optional[bool]=None, audio_new:Optional[bool]=None, video_new:Optional[bool]=None, wall_reply_new:Optional[bool]=None, wall_reply_edit:Optional[bool]=None, wall_reply_delete:Optional[bool]=None, wall_reply_restore:Optional[bool]=None, wall_post_new:Optional[bool]=None, wall_repost:Optional[bool]=None, board_post_new:Optional[bool]=None, board_post_edit:Optional[bool]=None, board_post_restore:Optional[bool]=None, board_post_delete:Optional[bool]=None, photo_comment_new:Optional[bool]=None, photo_comment_edit:Optional[bool]=None, photo_comment_delete:Optional[bool]=None, photo_comment_restore:Optional[bool]=None, video_comment_new:Optional[bool]=None, video_comment_edit:Optional[bool]=None, video_comment_delete:Optional[bool]=None, video_comment_restore:Optional[bool]=None, market_comment_new:Optional[bool]=None, market_comment_edit:Optional[bool]=None, market_comment_delete:Optional[bool]=None, market_comment_restore:Optional[bool]=None, poll_vote_new:Optional[bool]=None, group_join:Optional[bool]=None, group_leave:Optional[bool]=None, group_change_settings:Optional[bool]=None, group_change_photo:Optional[bool]=None, group_officers_edit:Optional[bool]=None, user_block:Optional[bool]=None, user_unblock:Optional[bool]=None, like_add:Optional[bool]=None, like_remove:Optional[bool]=None, message_event:Optional[bool]=None, donut_subscription_create:Optional[bool]=None, donut_subscription_prolonged:Optional[bool]=None, donut_subscription_cancelled:Optional[bool]=None, donut_subscription_price_changed:Optional[bool]=None, donut_subscription_expired:Optional[bool]=None, donut_money_withdraw:Optional[bool]=None, donut_money_withdraw_error:Optional[bool]=None):
		"""Sets Long Poll notification settings"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.setLongPollSettings", **args)
		return BaseOkResponse(**r)


	async def setSettings(self, group_id:Optional[int]=None, messages:Optional[bool]=None, bots_capabilities:Optional[bool]=None, bots_start_button:Optional[bool]=None, bots_add_to_chat:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.setSettings", **args)
		return BaseOkResponse(**r)


	async def setUserNote(self, group_id:Optional[int]=None, user_id:Optional[int]=None, note:Optional[str]=None):
		"""In order to save note about group participant"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.setUserNote", **args)
		return BaseBoolResponse(**r)


	async def tagAdd(self, group_id:Optional[int]=None, tag_name:Optional[str]=None, tag_color:Optional[str]=None):
		"""Add new group's tag"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.tagAdd", **args)
		return BaseBoolResponse(**r)


	async def tagBind(self, group_id:Optional[int]=None, tag_id:Optional[int]=None, user_id:Optional[int]=None, act:Optional[str]=None):
		"""Bind or unbind group's tag to user"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.tagBind", **args)
		return BaseBoolResponse(**r)


	async def tagDelete(self, group_id:Optional[int]=None, tag_id:Optional[int]=None):
		"""Delete group's tag"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.tagDelete", **args)
		return BaseBoolResponse(**r)


	async def tagUpdate(self, group_id:Optional[int]=None, tag_id:Optional[int]=None, tag_name:Optional[str]=None):
		"""Update group's tag"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.tagUpdate", **args)
		return BaseBoolResponse(**r)


	async def toggleMarket(self, group_id:Optional[int]=None, state:Optional[str]=None, ref:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.toggleMarket", **args)
		return BaseOkResponse(**r)


	async def unban(self, group_id:Optional[int]=None, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("groups.unban", **args)
		return BaseOkResponse(**r)



class Leadforms(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def create(self, group_id:Optional[int]=None, name:Optional[str]=None, title:Optional[str]=None, description:Optional[str]=None, questions:Optional[str]=None, policy_link_url:Optional[str]=None, photo:Optional[str]=None, confirmation:Optional[str]=None, site_link_url:Optional[str]=None, active:Optional[bool]=None, once_per_user:Optional[bool]=None, pixel_code:Optional[str]=None, notify_admins:Optional[list]=None, notify_emails:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.create", **args)
		return LeadFormsCreateResponse(**r)


	async def delete(self, group_id:Optional[int]=None, form_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.delete", **args)
		return LeadFormsDeleteResponse(**r)


	async def get(self, group_id:Optional[int]=None, form_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.get", **args)
		return LeadFormsGetResponse(**r)


	async def getLeads(self, group_id:Optional[int]=None, form_id:Optional[int]=None, limit:Optional[int]=None, next_page_token:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.getLeads", **args)
		return LeadFormsGetLeadsResponse(**r)


	async def getUploadURL(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.getUploadURL", **args)
		return LeadFormsUploadUrlResponse(**r)


	async def _list(self, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms._list", **args)
		return LeadFormsListResponse.parse_obj(r)


	async def update(self, group_id:Optional[int]=None, form_id:Optional[int]=None, name:Optional[str]=None, title:Optional[str]=None, description:Optional[str]=None, questions:Optional[str]=None, policy_link_url:Optional[str]=None, photo:Optional[str]=None, confirmation:Optional[str]=None, site_link_url:Optional[str]=None, active:Optional[bool]=None, once_per_user:Optional[bool]=None, pixel_code:Optional[str]=None, notify_admins:Optional[list]=None, notify_emails:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("leadforms.update", **args)
		return LeadFormsCreateResponse(**r)



class Likes(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None, access_key:Optional[str]=None):
		"""Adds the specified object to the 'Likes' list of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("likes.add", **args)
		return LikesAddResponse(**r)


	async def delete(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None, access_key:Optional[str]=None):
		"""Deletes the specified object from the 'Likes' list of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("likes.delete", **args)
		return LikesDeleteResponse(**r)


	async def getList(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None, page_url:Optional[str]=None, filter:Optional[str]=None, friends_only:Optional[int]=None, extended:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None, skip_own:Optional[bool]=None):
		"""Returns a list of IDs of users who added the specified object to their 'Likes' list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("likes.getList", **args)
		for i in [LikesGetListResponse, LikesGetListExtendedResponse]:
			try: return i(**r)
			except: return LikesGetListResponse(**r)


	async def isLiked(self, user_id:Optional[int]=None, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None):
		"""Checks for the object in the 'Likes' list of the specified user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("likes.isLiked", **args)
		return LikesIsLikedResponse(**r)



class Market(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, owner_id:Optional[int]=None, name:Optional[str]=None, description:Optional[str]=None, category_id:Optional[int]=None, price:Optional[int]=None, old_price:Optional[int]=None, deleted:Optional[bool]=None, main_photo_id:Optional[int]=None, photo_ids:Optional[list]=None, url:Optional[str]=None, dimension_width:Optional[int]=None, dimension_height:Optional[int]=None, dimension_length:Optional[int]=None, weight:Optional[int]=None, sku:Optional[str]=None):
		"""Ads a new item to the market."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.add", **args)
		return MarketAddResponse(**r)


	async def addAlbum(self, owner_id:Optional[int]=None, title:Optional[str]=None, photo_id:Optional[int]=None, main_album:Optional[bool]=None, is_hidden:Optional[bool]=None):
		"""Creates new collection of items"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.addAlbum", **args)
		return MarketAddAlbumResponse(**r)


	async def addToAlbum(self, owner_id:Optional[int]=None, item_ids:Optional[list]=None, album_ids:Optional[list]=None):
		"""Adds an item to one or multiple collections."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.addToAlbum", **args)
		return BaseOkResponse(**r)


	async def createComment(self, owner_id:Optional[int]=None, item_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, from_group:Optional[bool]=None, reply_to_comment:Optional[int]=None, sticker_id:Optional[int]=None, guid:Optional[str]=None):
		"""Creates a new comment for an item."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.createComment", **args)
		return MarketCreateCommentResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, item_id:Optional[int]=None):
		"""Deletes an item."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.delete", **args)
		return BaseOkResponse(**r)


	async def deleteAlbum(self, owner_id:Optional[int]=None, album_id:Optional[int]=None):
		"""Deletes a collection of items."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.deleteAlbum", **args)
		return BaseOkResponse(**r)


	async def deleteComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Deletes an item's comment"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.deleteComment", **args)
		return MarketDeleteCommentResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, item_id:Optional[int]=None, name:Optional[str]=None, description:Optional[str]=None, category_id:Optional[int]=None, price:Optional[int]=None, old_price:Optional[int]=None, deleted:Optional[bool]=None, main_photo_id:Optional[int]=None, photo_ids:Optional[list]=None, url:Optional[str]=None, dimension_width:Optional[int]=None, dimension_height:Optional[int]=None, dimension_length:Optional[int]=None, weight:Optional[int]=None, sku:Optional[str]=None):
		"""Edits an item."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.edit", **args)
		return BaseOkResponse(**r)


	async def editAlbum(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, title:Optional[str]=None, photo_id:Optional[int]=None, main_album:Optional[bool]=None, is_hidden:Optional[bool]=None):
		"""Edits a collection of items"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.editAlbum", **args)
		return BaseOkResponse(**r)


	async def editComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None):
		"""Chages item comment's text"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.editComment", **args)
		return BaseOkResponse(**r)


	async def editOrder(self, user_id:Optional[int]=None, order_id:Optional[int]=None, merchant_comment:Optional[str]=None, status:Optional[int]=None, track_number:Optional[str]=None, payment_status:Optional[str]=None, delivery_price:Optional[int]=None, width:Optional[int]=None, length:Optional[int]=None, height:Optional[int]=None, weight:Optional[int]=None):
		"""Edit order"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.editOrder", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, count:Optional[int]=None, offset:Optional[int]=None, extended:Optional[bool]=None, date_from:Optional[str]=None, date_to:Optional[str]=None, need_variants:Optional[bool]=None, with_disabled:Optional[bool]=None):
		"""Returns items list for a community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.get", **args)
		for i in [MarketGetResponse, MarketGetExtendedResponse]:
			try: return i(**r)
			except: return MarketGetResponse(**r)


	async def getAlbumById(self, owner_id:Optional[int]=None, album_ids:Optional[list]=None):
		"""Returns items album's data"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getAlbumById", **args)
		return MarketGetAlbumByIdResponse(**r)


	async def getAlbums(self, owner_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns community's market collections list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getAlbums", **args)
		return MarketGetAlbumsResponse(**r)


	async def getById(self, item_ids:Optional[list]=None, extended:Optional[bool]=None):
		"""Returns information about market items by their ids."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getById", **args)
		for i in [MarketGetByIdResponse, MarketGetByIdExtendedResponse]:
			try: return i(**r)
			except: return MarketGetByIdResponse(**r)


	async def getCategories(self, count:Optional[int]=None, offset:Optional[int]=None):
		"""Returns a list of market categories."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getCategories", **args)
		return MarketGetCategoriesResponse(**r)


	async def getComments(self, owner_id:Optional[int]=None, item_id:Optional[int]=None, need_likes:Optional[bool]=None, start_comment_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, sort:Optional[str]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns comments list for an item."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getComments", **args)
		return MarketGetCommentsResponse(**r)


	async def getGroupOrders(self, group_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Get market orders"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getGroupOrders", **args)
		return MarketGetGroupOrdersResponse(**r)


	async def getOrderById(self, user_id:Optional[int]=None, order_id:Optional[int]=None, extended:Optional[bool]=None):
		"""Get order"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getOrderById", **args)
		return MarketGetOrderByIdResponse(**r)


	async def getOrderItems(self, user_id:Optional[int]=None, order_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Get market items in the order"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getOrderItems", **args)
		return MarketGetOrderItemsResponse(**r)


	async def getOrders(self, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, date_from:Optional[str]=None, date_to:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.getOrders", **args)
		for i in [MarketGetOrdersResponse, MarketGetOrdersExtendedResponse]:
			try: return i(**r)
			except: return MarketGetOrdersResponse(**r)


	async def removeFromAlbum(self, owner_id:Optional[int]=None, item_id:Optional[int]=None, album_ids:Optional[list]=None):
		"""Removes an item from one or multiple collections."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.removeFromAlbum", **args)
		return BaseOkResponse(**r)


	async def reorderAlbums(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, before:Optional[int]=None, after:Optional[int]=None):
		"""Reorders the collections list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.reorderAlbums", **args)
		return BaseOkResponse(**r)


	async def reorderItems(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, item_id:Optional[int]=None, before:Optional[int]=None, after:Optional[int]=None):
		"""Changes item place in a collection."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.reorderItems", **args)
		return BaseOkResponse(**r)


	async def report(self, owner_id:Optional[int]=None, item_id:Optional[int]=None, reason:Optional[int]=None):
		"""Sends a complaint to the item."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.report", **args)
		return BaseOkResponse(**r)


	async def reportComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, reason:Optional[int]=None):
		"""Sends a complaint to the item's comment."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.reportComment", **args)
		return BaseOkResponse(**r)


	async def restore(self, owner_id:Optional[int]=None, item_id:Optional[int]=None):
		"""Restores recently deleted item"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.restore", **args)
		return BaseOkResponse(**r)


	async def restoreComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Restores a recently deleted comment"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.restoreComment", **args)
		return MarketRestoreCommentResponse(**r)


	async def search(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, q:Optional[str]=None, price_from:Optional[int]=None, price_to:Optional[int]=None, sort:Optional[int]=None, rev:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, status:Optional[list]=None, need_variants:Optional[bool]=None):
		"""Searches market items in a community's catalog"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.search", **args)
		for i in [MarketSearchResponse, MarketSearchExtendedResponse]:
			try: return i(**r)
			except: return MarketSearchResponse(**r)


	async def searchItems(self, q:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None, category_id:Optional[int]=None, price_from:Optional[int]=None, price_to:Optional[int]=None, sort_by:Optional[int]=None, sort_direction:Optional[int]=None, country:Optional[int]=None, city:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("market.searchItems", **args)
		return MarketSearchResponse(**r)



class Messages(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addChatUser(self, chat_id:Optional[int]=None, user_id:Optional[int]=None, visible_messages_count:Optional[int]=None):
		"""Adds a new user to a chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.addChatUser", **args)
		return BaseOkResponse(**r)


	async def allowMessagesFromGroup(self, group_id:Optional[int]=None, key:Optional[str]=None):
		"""Allows sending messages from community to the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.allowMessagesFromGroup", **args)
		return BaseOkResponse(**r)


	async def createChat(self, user_ids:Optional[list]=None, title:Optional[str]=None, group_id:Optional[int]=None):
		"""Creates a chat with several participants."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.createChat", **args)
		return MessagesCreateChatResponse(**r)


	async def delete(self, message_ids:Optional[list]=None, spam:Optional[bool]=None, group_id:Optional[int]=None, delete_for_all:Optional[bool]=None, peer_id:Optional[int]=None, cmids:Optional[list]=None):
		"""Deletes one or more messages."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.delete", **args)
		return MessagesDeleteResponse(**r)


	async def deleteChatPhoto(self, chat_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Deletes a chat's cover picture."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.deleteChatPhoto", **args)
		return MessagesDeleteChatPhotoResponse(**r)


	async def deleteConversation(self, user_id:Optional[int]=None, peer_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Deletes all private messages in a conversation."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.deleteConversation", **args)
		return MessagesDeleteConversationResponse(**r)


	async def denyMessagesFromGroup(self, group_id:Optional[int]=None):
		"""Denies sending message from community to the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.denyMessagesFromGroup", **args)
		return BaseOkResponse(**r)


	async def edit(self, peer_id:Optional[int]=None, message:Optional[str]=None, lat:Optional[int]=None, long:Optional[int]=None, attachment:Optional[str]=None, keep_forward_messages:Optional[bool]=None, keep_snippets:Optional[bool]=None, group_id:Optional[int]=None, dont_parse_links:Optional[bool]=None, disable_mentions:Optional[bool]=None, message_id:Optional[int]=None, conversation_message_id:Optional[int]=None, template:Optional[str]=None, keyboard:Optional[str]=None):
		"""Edits the message."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.edit", **args)
		return MessagesEditResponse(**r)


	async def editChat(self, chat_id:Optional[int]=None, title:Optional[str]=None):
		"""Edits the title of a chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.editChat", **args)
		return BaseOkResponse(**r)


	async def getByConversationMessageId(self, peer_id:Optional[int]=None, conversation_message_ids:Optional[list]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns messages by their IDs within the conversation."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getByConversationMessageId", **args)
		for i in [MessagesGetByConversationMessageIdResponse, MessagesGetByConversationMessageIdExtendedResponse]:
			try: return i(**r)
			except: return MessagesGetByConversationMessageIdResponse(**r)


	async def getById(self, message_ids:Optional[list]=None, preview_length:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns messages by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getById", **args)
		for i in [MessagesGetByIdResponse, MessagesGetByIdExtendedResponse]:
			try: return i(**r)
			except: return MessagesGetByIdResponse(**r)


	async def getChatPreview(self, peer_id:Optional[int]=None, link:Optional[str]=None, fields:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getChatPreview", **args)
		return MessagesGetChatPreviewResponse(**r)


	async def getConversationMembers(self, peer_id:Optional[int]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns a list of IDs of users participating in a chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getConversationMembers", **args)
		return MessagesGetConversationMembersResponse(**r)


	async def getConversations(self, offset:Optional[int]=None, count:Optional[int]=None, filter:Optional[str]=None, extended:Optional[bool]=None, start_message_id:Optional[int]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns a list of the current user's conversations."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getConversations", **args)
		return MessagesGetConversationsResponse(**r)


	async def getConversationsById(self, peer_ids:Optional[list]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns conversations by their IDs"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getConversationsById", **args)
		for i in [MessagesGetConversationsByIdResponse, MessagesGetConversationsByIdExtendedResponse]:
			try: return i(**r)
			except: return MessagesGetConversationsByIdResponse(**r)


	async def getHistory(self, offset:Optional[int]=None, count:Optional[int]=None, user_id:Optional[int]=None, peer_id:Optional[int]=None, start_message_id:Optional[int]=None, rev:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns message history for the specified user or group chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getHistory", **args)
		for i in [MessagesGetHistoryResponse, MessagesGetHistoryExtendedResponse]:
			try: return i(**r)
			except: return MessagesGetHistoryResponse(**r)


	async def getHistoryAttachments(self, peer_id:Optional[int]=None, media_type:Optional[str]=None, start_from:Optional[str]=None, count:Optional[int]=None, photo_sizes:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None, preserve_order:Optional[bool]=None, max_forwards_level:Optional[int]=None):
		"""Returns media files from the dialog or group chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getHistoryAttachments", **args)
		return MessagesGetHistoryAttachmentsResponse(**r)


	async def getImportantMessages(self, count:Optional[int]=None, offset:Optional[int]=None, start_message_id:Optional[int]=None, preview_length:Optional[int]=None, fields:Optional[list]=None, extended:Optional[bool]=None, group_id:Optional[int]=None):
		"""Returns a list of user's important messages."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getImportantMessages", **args)
		for i in [MessagesGetImportantMessagesResponse, MessagesGetImportantMessagesExtendedResponse]:
			try: return i(**r)
			except: return MessagesGetImportantMessagesResponse(**r)


	async def getIntentUsers(self, intent:Optional[str]=None, subscribe_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, name_case:Optional[list]=None, fields:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getIntentUsers", **args)
		return MessagesGetIntentUsersResponse(**r)


	async def getInviteLink(self, peer_id:Optional[int]=None, reset:Optional[bool]=None, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getInviteLink", **args)
		return MessagesGetInviteLinkResponse(**r)


	async def getLastActivity(self, user_id:Optional[int]=None):
		"""Returns a user's current status and date of last activity."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getLastActivity", **args)
		return MessagesGetLastActivityResponse(**r)


	async def getLongPollHistory(self, ts:Optional[int]=None, pts:Optional[int]=None, preview_length:Optional[int]=None, onlines:Optional[bool]=None, fields:Optional[list]=None, events_limit:Optional[int]=None, msgs_limit:Optional[int]=None, max_msg_id:Optional[int]=None, group_id:Optional[int]=None, lp_version:Optional[int]=None, last_n:Optional[int]=None, credentials:Optional[bool]=None, extended:Optional[bool]=None):
		"""Returns updates in user's private messages."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getLongPollHistory", **args)
		return MessagesGetLongPollHistoryResponse(**r)


	async def getLongPollServer(self, need_pts:Optional[bool]=None, group_id:Optional[int]=None, lp_version:Optional[int]=None):
		"""Returns data required for connection to a Long Poll server."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.getLongPollServer", **args)
		return MessagesGetLongPollServerResponse(**r)


	async def isMessagesFromGroupAllowed(self, group_id:Optional[int]=None, user_id:Optional[int]=None):
		"""Returns information whether sending messages from the community to current user is allowed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.isMessagesFromGroupAllowed", **args)
		return MessagesIsMessagesFromGroupAllowedResponse(**r)


	async def joinChatByInviteLink(self, link:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.joinChatByInviteLink", **args)
		return MessagesJoinChatByInviteLinkResponse(**r)


	async def markAsAnsweredConversation(self, peer_id:Optional[int]=None, answered:Optional[bool]=None, group_id:Optional[int]=None):
		"""Marks and unmarks conversations as unanswered."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.markAsAnsweredConversation", **args)
		return BaseOkResponse(**r)


	async def markAsImportant(self, message_ids:Optional[list]=None, important:Optional[int]=None):
		"""Marks and unmarks messages as important (starred)."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.markAsImportant", **args)
		return MessagesMarkAsImportantResponse.parse_obj(r)


	async def markAsImportantConversation(self, peer_id:Optional[int]=None, important:Optional[bool]=None, group_id:Optional[int]=None):
		"""Marks and unmarks conversations as important."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.markAsImportantConversation", **args)
		return BaseOkResponse(**r)


	async def markAsRead(self, message_ids:Optional[list]=None, peer_id:Optional[int]=None, start_message_id:Optional[int]=None, group_id:Optional[int]=None, mark_conversation_as_read:Optional[bool]=None):
		"""Marks messages as read."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.markAsRead", **args)
		return BaseOkResponse(**r)


	async def pin(self, peer_id:Optional[int]=None, message_id:Optional[int]=None, conversation_message_id:Optional[int]=None):
		"""Pin a message."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.pin", **args)
		return MessagesPinResponse(**r)


	async def removeChatUser(self, chat_id:Optional[int]=None, user_id:Optional[int]=None, member_id:Optional[int]=None):
		"""Allows the current user to leave a chat or, if the current user started the chat, allows the user to remove another user from the chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.removeChatUser", **args)
		return BaseOkResponse(**r)


	async def restore(self, message_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Restores a deleted message."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.restore", **args)
		return BaseOkResponse(**r)


	async def search(self, q:Optional[str]=None, peer_id:Optional[int]=None, date:Optional[int]=None, preview_length:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns a list of the current user's private messages that match search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.search", **args)
		for i in [MessagesSearchResponse, MessagesSearchExtendedResponse]:
			try: return i(**r)
			except: return MessagesSearchResponse(**r)


	async def searchConversations(self, q:Optional[str]=None, count:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None, group_id:Optional[int]=None):
		"""Returns a list of the current user's conversations that match search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.searchConversations", **args)
		for i in [MessagesSearchConversationsResponse, MessagesSearchConversationsExtendedResponse]:
			try: return i(**r)
			except: return MessagesSearchConversationsResponse(**r)


	async def send(self, user_id:Optional[int]=None, random_id:Optional[int]=None, peer_id:Optional[int]=None, peer_ids:Optional[list]=None, domain:Optional[str]=None, chat_id:Optional[int]=None, user_ids:Optional[list]=None, message:Optional[str]=None, lat:Optional[int]=None, long:Optional[int]=None, attachment:Optional[str]=None, reply_to:Optional[int]=None, forward_messages:Optional[list]=None, forward:Optional[str]=None, sticker_id:Optional[int]=None, group_id:Optional[int]=None, keyboard:Optional[str]=None, template:Optional[str]=None, payload:Optional[str]=None, content_source:Optional[str]=None, dont_parse_links:Optional[bool]=None, disable_mentions:Optional[bool]=None, intent:Optional[str]=None, subscribe_id:Optional[int]=None):
		"""Sends a message."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.send", **args)
		for i in [MessagesSendResponse, MessagesSendUserIdsResponse]:
			try: return i(**r)
			except: return MessagesSendResponse(**r)


	async def sendMessageEventAnswer(self, event_id:Optional[str]=None, user_id:Optional[int]=None, peer_id:Optional[int]=None, event_data:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.sendMessageEventAnswer", **args)
		return BaseOkResponse(**r)


	async def setActivity(self, user_id:Optional[int]=None, type:Optional[str]=None, peer_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Changes the status of a user as typing in a conversation."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.setActivity", **args)
		return BaseOkResponse(**r)


	async def setChatPhoto(self, file:Optional[str]=None):
		"""Sets a previously-uploaded picture as the cover picture of a chat."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.setChatPhoto", **args)
		return MessagesSetChatPhotoResponse(**r)


	async def unpin(self, peer_id:Optional[int]=None, group_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("messages.unpin", **args)
		return BaseOkResponse(**r)



class Newsfeed(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addBan(self, user_ids:Optional[list]=None, group_ids:Optional[list]=None):
		"""Prevents news from specified users and communities from appearing in the current user's newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.addBan", **args)
		return BaseOkResponse(**r)


	async def deleteBan(self, user_ids:Optional[list]=None, group_ids:Optional[list]=None):
		"""Allows news from previously banned users and communities to be shown in the current user's newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.deleteBan", **args)
		return BaseOkResponse(**r)


	async def deleteList(self, list_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.deleteList", **args)
		return BaseOkResponse(**r)


	async def get(self, filters:Optional[list]=None, return_banned:Optional[bool]=None, start_time:Optional[int]=None, end_time:Optional[int]=None, max_photos:Optional[int]=None, source_ids:Optional[str]=None, start_from:Optional[str]=None, count:Optional[int]=None, fields:Optional[list]=None, section:Optional[str]=None):
		"""Returns data required to show newsfeed for the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.get", **args)
		return NewsfeedGenericResponse(**r)


	async def getBanned(self, extended:Optional[bool]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns a list of users and communities banned from the current user's newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getBanned", **args)
		for i in [NewsfeedGetBannedResponse, NewsfeedGetBannedExtendedResponse]:
			try: return i(**r)
			except: return NewsfeedGetBannedResponse(**r)


	async def getComments(self, count:Optional[int]=None, filters:Optional[list]=None, reposts:Optional[str]=None, start_time:Optional[int]=None, end_time:Optional[int]=None, last_comments_count:Optional[int]=None, start_from:Optional[str]=None, fields:Optional[list]=None):
		"""Returns a list of comments in the current user's newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getComments", **args)
		return NewsfeedGetCommentsResponse(**r)


	async def getLists(self, list_ids:Optional[list]=None, extended:Optional[bool]=None):
		"""Returns a list of newsfeeds followed by the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getLists", **args)
		for i in [NewsfeedGetListsResponse, NewsfeedGetListsExtendedResponse]:
			try: return i(**r)
			except: return NewsfeedGetListsResponse(**r)


	async def getMentions(self, owner_id:Optional[int]=None, start_time:Optional[int]=None, end_time:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of posts on user walls in which the current user is mentioned."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getMentions", **args)
		return NewsfeedGetMentionsResponse(**r)


	async def getRecommended(self, start_time:Optional[int]=None, end_time:Optional[int]=None, max_photos:Optional[int]=None, start_from:Optional[str]=None, count:Optional[int]=None, fields:Optional[list]=None):
		""", Returns a list of newsfeeds recommended to the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getRecommended", **args)
		return NewsfeedGenericResponse(**r)


	async def getSuggestedSources(self, offset:Optional[int]=None, count:Optional[int]=None, shuffle:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns communities and users that current user is suggested to follow."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.getSuggestedSources", **args)
		return NewsfeedGetSuggestedSourcesResponse(**r)


	async def ignoreItem(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None):
		"""Hides an item from the newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.ignoreItem", **args)
		return BaseOkResponse(**r)


	async def saveList(self, list_id:Optional[int]=None, title:Optional[str]=None, source_ids:Optional[list]=None, no_reposts:Optional[bool]=None):
		"""Creates and edits user newsfeed lists"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.saveList", **args)
		return NewsfeedSaveListResponse(**r)


	async def search(self, q:Optional[str]=None, extended:Optional[bool]=None, count:Optional[int]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, start_time:Optional[int]=None, end_time:Optional[int]=None, start_from:Optional[str]=None, fields:Optional[list]=None):
		"""Returns search results by statuses."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.search", **args)
		for i in [NewsfeedSearchResponse, NewsfeedSearchExtendedResponse]:
			try: return i(**r)
			except: return NewsfeedSearchResponse(**r)


	async def unignoreItem(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None, track_code:Optional[str]=None):
		"""Returns a hidden item to the newsfeed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.unignoreItem", **args)
		return BaseOkResponse(**r)


	async def unsubscribe(self, type:Optional[str]=None, owner_id:Optional[int]=None, item_id:Optional[int]=None):
		"""Unsubscribes the current user from specified newsfeeds."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("newsfeed.unsubscribe", **args)
		return BaseOkResponse(**r)



class Notes(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, title:Optional[str]=None, text:Optional[str]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None):
		"""Creates a new note for the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.add", **args)
		return NotesAddResponse(**r)


	async def createComment(self, note_id:Optional[int]=None, owner_id:Optional[int]=None, reply_to:Optional[int]=None, message:Optional[str]=None, guid:Optional[str]=None):
		"""Adds a new comment on a note."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.createComment", **args)
		return NotesCreateCommentResponse(**r)


	async def delete(self, note_id:Optional[int]=None):
		"""Deletes a note of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.delete", **args)
		return BaseOkResponse(**r)


	async def deleteComment(self, comment_id:Optional[int]=None, owner_id:Optional[int]=None):
		"""Deletes a comment on a note."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.deleteComment", **args)
		return BaseOkResponse(**r)


	async def edit(self, note_id:Optional[int]=None, title:Optional[str]=None, text:Optional[str]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None):
		"""Edits a note of the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.edit", **args)
		return BaseOkResponse(**r)


	async def editComment(self, comment_id:Optional[int]=None, owner_id:Optional[int]=None, message:Optional[str]=None):
		"""Edits a comment on a note."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.editComment", **args)
		return BaseOkResponse(**r)


	async def get(self, note_ids:Optional[list]=None, user_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, sort:Optional[int]=None):
		"""Returns a list of notes created by a user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.get", **args)
		return NotesGetResponse(**r)


	async def getById(self, note_id:Optional[int]=None, owner_id:Optional[int]=None, need_wiki:Optional[bool]=None):
		"""Returns a note by its ID."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.getById", **args)
		return NotesGetByIdResponse(**r)


	async def getComments(self, note_id:Optional[int]=None, owner_id:Optional[int]=None, sort:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of comments on a note."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.getComments", **args)
		return NotesGetCommentsResponse(**r)


	async def restoreComment(self, comment_id:Optional[int]=None, owner_id:Optional[int]=None):
		"""Restores a deleted comment on a note."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notes.restoreComment", **args)
		return BaseOkResponse(**r)



class Notifications(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, count:Optional[int]=None, start_from:Optional[str]=None, filters:Optional[list]=None, start_time:Optional[int]=None, end_time:Optional[int]=None):
		"""Returns a list of notifications about other users' feedback to the current user's wall posts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notifications.get", **args)
		return NotificationsGetResponse(**r)


	async def markAsViewed(self):
		"""Resets the counter of new notifications about other users' feedback to the current user's wall posts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notifications.markAsViewed", **args)
		return NotificationsMarkAsViewedResponse(**r)


	async def sendMessage(self, user_ids:Optional[list]=None, message:Optional[str]=None, fragment:Optional[str]=None, group_id:Optional[int]=None, random_id:Optional[int]=None, sending_mode:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("notifications.sendMessage", **args)
		return NotificationsSendMessageResponse.parse_obj(r)



class Orders(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def cancelSubscription(self, user_id:Optional[int]=None, subscription_id:Optional[int]=None, pending_cancel:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.cancelSubscription", **args)
		return OrdersCancelSubscriptionResponse(**r)


	async def changeState(self, order_id:Optional[int]=None, action:Optional[str]=None, app_order_id:Optional[int]=None, test_mode:Optional[bool]=None):
		"""Changes order status."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.changeState", **args)
		return OrdersChangeStateResponse(**r)


	async def get(self, offset:Optional[int]=None, count:Optional[int]=None, test_mode:Optional[bool]=None):
		"""Returns a list of orders."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.get", **args)
		return OrdersGetResponse.parse_obj(r)


	async def getAmount(self, user_id:Optional[int]=None, votes:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.getAmount", **args)
		return OrdersGetAmountResponse.parse_obj(r)


	async def getById(self, order_id:Optional[int]=None, order_ids:Optional[list]=None, test_mode:Optional[bool]=None):
		"""Returns information about orders by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.getById", **args)
		return OrdersGetByIdResponse.parse_obj(r)


	async def getUserSubscriptionById(self, user_id:Optional[int]=None, subscription_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.getUserSubscriptionById", **args)
		return OrdersGetUserSubscriptionByIdResponse(**r)


	async def getUserSubscriptions(self, user_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.getUserSubscriptions", **args)
		return OrdersGetUserSubscriptionsResponse(**r)


	async def updateSubscription(self, user_id:Optional[int]=None, subscription_id:Optional[int]=None, price:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("orders.updateSubscription", **args)
		return OrdersUpdateSubscriptionResponse(**r)



class Pages(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def clearCache(self, url:Optional[str]=None):
		"""Allows to clear the cache of particular 'external' pages which may be attached to VK posts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.clearCache", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, page_id:Optional[int]=None, _global:Optional[bool]=None, site_preview:Optional[bool]=None, title:Optional[str]=None, need_source:Optional[bool]=None, need_html:Optional[bool]=None):
		"""Returns information about a wiki page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.get", **args)
		return PagesGetResponse(**r)


	async def getHistory(self, page_id:Optional[int]=None, group_id:Optional[int]=None, user_id:Optional[int]=None):
		"""Returns a list of all previous versions of a wiki page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.getHistory", **args)
		return PagesGetHistoryResponse.parse_obj(r)


	async def getTitles(self, group_id:Optional[int]=None):
		"""Returns a list of wiki pages in a group."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.getTitles", **args)
		return PagesGetTitlesResponse.parse_obj(r)


	async def getVersion(self, version_id:Optional[int]=None, group_id:Optional[int]=None, user_id:Optional[int]=None, need_html:Optional[bool]=None):
		"""Returns the text of one of the previous versions of a wiki page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.getVersion", **args)
		return PagesGetVersionResponse(**r)


	async def parseWiki(self, text:Optional[str]=None, group_id:Optional[int]=None):
		"""Returns HTML representation of the wiki markup."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.parseWiki", **args)
		return PagesParseWikiResponse(**r)


	async def save(self, text:Optional[str]=None, page_id:Optional[int]=None, group_id:Optional[int]=None, user_id:Optional[int]=None, title:Optional[str]=None):
		"""Saves the text of a wiki page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.save", **args)
		return PagesSaveResponse(**r)


	async def saveAccess(self, page_id:Optional[int]=None, group_id:Optional[int]=None, user_id:Optional[int]=None, view:Optional[int]=None, edit:Optional[int]=None):
		"""Saves modified read and edit access settings for a wiki page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("pages.saveAccess", **args)
		return PagesSaveAccessResponse(**r)



class Photos(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def confirmTag(self, owner_id:Optional[int]=None, photo_id:Optional[str]=None, tag_id:Optional[int]=None):
		"""Confirms a tag on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.confirmTag", **args)
		return BaseOkResponse(**r)


	async def copy(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, access_key:Optional[str]=None):
		"""Allows to copy a photo to the 'Saved photos' album"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.copy", **args)
		return PhotosCopyResponse(**r)


	async def createAlbum(self, title:Optional[str]=None, group_id:Optional[int]=None, description:Optional[str]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None, upload_by_admins_only:Optional[bool]=None, comments_disabled:Optional[bool]=None):
		"""Creates an empty photo album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.createAlbum", **args)
		return PhotosCreateAlbumResponse(**r)


	async def createComment(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, from_group:Optional[bool]=None, reply_to_comment:Optional[int]=None, sticker_id:Optional[int]=None, access_key:Optional[str]=None, guid:Optional[str]=None):
		"""Adds a new comment on the photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.createComment", **args)
		return PhotosCreateCommentResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None):
		"""Deletes a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.delete", **args)
		return BaseOkResponse(**r)


	async def deleteAlbum(self, album_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Deletes a photo album belonging to the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.deleteAlbum", **args)
		return BaseOkResponse(**r)


	async def deleteComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Deletes a comment on the photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.deleteComment", **args)
		return PhotosDeleteCommentResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, caption:Optional[str]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, place_str:Optional[str]=None, foursquare_id:Optional[str]=None, delete_place:Optional[bool]=None):
		"""Edits the caption of a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.edit", **args)
		return BaseOkResponse(**r)


	async def editAlbum(self, album_id:Optional[int]=None, title:Optional[str]=None, description:Optional[str]=None, owner_id:Optional[int]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None, upload_by_admins_only:Optional[bool]=None, comments_disabled:Optional[bool]=None):
		"""Edits information about a photo album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.editAlbum", **args)
		return BaseOkResponse(**r)


	async def editComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None):
		"""Edits a comment on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.editComment", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, album_id:Optional[str]=None, photo_ids:Optional[list]=None, rev:Optional[bool]=None, extended:Optional[bool]=None, feed_type:Optional[str]=None, feed:Optional[int]=None, photo_sizes:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of a user's or community's photos."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.get", **args)
		return PhotosGetResponse(**r)


	async def getAlbums(self, owner_id:Optional[int]=None, album_ids:Optional[list]=None, offset:Optional[int]=None, count:Optional[int]=None, need_system:Optional[bool]=None, need_covers:Optional[bool]=None, photo_sizes:Optional[bool]=None):
		"""Returns a list of a user's or community's photo albums."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getAlbums", **args)
		return PhotosGetAlbumsResponse(**r)


	async def getAlbumsCount(self, user_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Returns the number of photo albums belonging to a user or community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getAlbumsCount", **args)
		return PhotosGetAlbumsCountResponse(**r)


	async def getAll(self, owner_id:Optional[int]=None, extended:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None, photo_sizes:Optional[bool]=None, no_service_albums:Optional[bool]=None, need_hidden:Optional[bool]=None, skip_hidden:Optional[bool]=None):
		"""Returns a list of photos belonging to a user or community, in reverse chronological order."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getAll", **args)
		for i in [PhotosGetAllResponse, PhotosGetAllExtendedResponse]:
			try: return i(**r)
			except: return PhotosGetAllResponse(**r)


	async def getAllComments(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, need_likes:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of comments on a specific photo album or all albums of the user sorted in reverse chronological order."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getAllComments", **args)
		return PhotosGetAllCommentsResponse(**r)


	async def getById(self, photos:Optional[list]=None, extended:Optional[bool]=None, photo_sizes:Optional[bool]=None):
		"""Returns information about photos by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getById", **args)
		return PhotosGetByIdResponse.parse_obj(r)


	async def getChatUploadServer(self, chat_id:Optional[int]=None, crop_x:Optional[int]=None, crop_y:Optional[int]=None, crop_width:Optional[int]=None):
		"""Returns an upload link for chat cover pictures."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getChatUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def getComments(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, need_likes:Optional[bool]=None, start_comment_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, sort:Optional[str]=None, access_key:Optional[str]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns a list of comments on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getComments", **args)
		for i in [PhotosGetCommentsResponse, PhotosGetCommentsExtendedResponse]:
			try: return i(**r)
			except: return PhotosGetCommentsResponse(**r)


	async def getMarketAlbumUploadServer(self, group_id:Optional[int]=None):
		"""Returns the server address for market album photo upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getMarketAlbumUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def getMarketUploadServer(self, group_id:Optional[int]=None, main_photo:Optional[bool]=None, crop_x:Optional[int]=None, crop_y:Optional[int]=None, crop_width:Optional[int]=None):
		"""Returns the server address for market photo upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getMarketUploadServer", **args)
		return PhotosGetMarketUploadServerResponse(**r)


	async def getMessagesUploadServer(self, peer_id:Optional[int]=None):
		"""Returns the server address for photo upload in a private message for a user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getMessagesUploadServer", **args)
		return PhotosGetMessagesUploadServerResponse(**r)


	async def getNewTags(self, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns a list of photos with tags that have not been viewed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getNewTags", **args)
		return PhotosGetNewTagsResponse(**r)


	async def getOwnerCoverPhotoUploadServer(self, group_id:Optional[int]=None, crop_x:Optional[int]=None, crop_y:Optional[int]=None, crop_x2:Optional[int]=None, crop_y2:Optional[int]=None):
		"""Returns the server address for owner cover upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getOwnerCoverPhotoUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def getOwnerPhotoUploadServer(self, owner_id:Optional[int]=None):
		"""Returns an upload server address for a profile or community photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getOwnerPhotoUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def getTags(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, access_key:Optional[str]=None):
		"""Returns a list of tags on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getTags", **args)
		return PhotosGetTagsResponse.parse_obj(r)


	async def getUploadServer(self, album_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Returns the server address for photo upload."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getUploadServer", **args)
		return PhotosGetUploadServerResponse(**r)


	async def getUserPhotos(self, user_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, sort:Optional[str]=None):
		"""Returns a list of photos in which a user is tagged."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getUserPhotos", **args)
		return PhotosGetUserPhotosResponse(**r)


	async def getWallUploadServer(self, group_id:Optional[int]=None):
		"""Returns the server address for photo upload onto a user's wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.getWallUploadServer", **args)
		return PhotosGetWallUploadServerResponse(**r)


	async def makeCover(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, album_id:Optional[int]=None):
		"""Makes a photo into an album cover."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.makeCover", **args)
		return BaseOkResponse(**r)


	async def move(self, owner_id:Optional[int]=None, target_album_id:Optional[int]=None, photo_ids:Optional[int]=None):
		"""Moves a photo from one album to another."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.move", **args)
		return BaseOkResponse(**r)


	async def putTag(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, user_id:Optional[int]=None, x:Optional[int]=None, y:Optional[int]=None, x2:Optional[int]=None, y2:Optional[int]=None):
		"""Adds a tag on the photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.putTag", **args)
		return PhotosPutTagResponse(**r)


	async def removeTag(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, tag_id:Optional[int]=None):
		"""Removes a tag from a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.removeTag", **args)
		return BaseOkResponse(**r)


	async def reorderAlbums(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, before:Optional[int]=None, after:Optional[int]=None):
		"""Reorders the album in the list of user albums."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.reorderAlbums", **args)
		return BaseOkResponse(**r)


	async def reorderPhotos(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, before:Optional[int]=None, after:Optional[int]=None):
		"""Reorders the photo in the list of photos of the user album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.reorderPhotos", **args)
		return BaseOkResponse(**r)


	async def report(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None, reason:Optional[int]=None):
		"""Reports (submits a complaint about) a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.report", **args)
		return BaseOkResponse(**r)


	async def reportComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, reason:Optional[int]=None):
		"""Reports (submits a complaint about) a comment on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.reportComment", **args)
		return BaseOkResponse(**r)


	async def restore(self, owner_id:Optional[int]=None, photo_id:Optional[int]=None):
		"""Restores a deleted photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.restore", **args)
		return BaseOkResponse(**r)


	async def restoreComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Restores a deleted comment on a photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.restoreComment", **args)
		return PhotosRestoreCommentResponse(**r)


	async def save(self, album_id:Optional[int]=None, group_id:Optional[int]=None, server:Optional[int]=None, photos_list:Optional[str]=None, hash:Optional[str]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, caption:Optional[str]=None):
		"""Saves photos after successful uploading."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.save", **args)
		return PhotosSaveResponse.parse_obj(r)


	async def saveMarketAlbumPhoto(self, group_id:Optional[int]=None, photo:Optional[str]=None, server:Optional[int]=None, hash:Optional[str]=None):
		"""Saves market album photos after successful uploading."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveMarketAlbumPhoto", **args)
		return PhotosSaveMarketAlbumPhotoResponse.parse_obj(r)


	async def saveMarketPhoto(self, group_id:Optional[int]=None, photo:Optional[str]=None, server:Optional[int]=None, hash:Optional[str]=None, crop_data:Optional[str]=None, crop_hash:Optional[str]=None):
		"""Saves market photos after successful uploading."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveMarketPhoto", **args)
		return PhotosSaveMarketPhotoResponse.parse_obj(r)


	async def saveMessagesPhoto(self, photo:Optional[str]=None, server:Optional[int]=None, hash:Optional[str]=None):
		"""Saves a photo after being successfully uploaded. URL obtained with [vk.com/dev/photos.getMessagesUploadServer|photos.getMessagesUploadServer] method."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveMessagesPhoto", **args)
		return PhotosSaveMessagesPhotoResponse.parse_obj(r)


	async def saveOwnerCoverPhoto(self, hash:Optional[str]=None, photo:Optional[str]=None):
		"""Saves cover photo after successful uploading."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveOwnerCoverPhoto", **args)
		return PhotosSaveOwnerCoverPhotoResponse(**r)


	async def saveOwnerPhoto(self, server:Optional[str]=None, hash:Optional[str]=None, photo:Optional[str]=None):
		"""Saves a profile or community photo. Upload URL can be got with the [vk.com/dev/photos.getOwnerPhotoUploadServer|photos.getOwnerPhotoUploadServer] method."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveOwnerPhoto", **args)
		return PhotosSaveOwnerPhotoResponse(**r)


	async def saveWallPhoto(self, user_id:Optional[int]=None, group_id:Optional[int]=None, photo:Optional[str]=None, server:Optional[int]=None, hash:Optional[str]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, caption:Optional[str]=None):
		"""Saves a photo to a user's or community's wall after being uploaded."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.saveWallPhoto", **args)
		return PhotosSaveWallPhotoResponse.parse_obj(r)


	async def search(self, q:Optional[str]=None, lat:Optional[int]=None, long:Optional[int]=None, start_time:Optional[int]=None, end_time:Optional[int]=None, sort:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, radius:Optional[int]=None):
		"""Returns a list of photos."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("photos.search", **args)
		return PhotosSearchResponse(**r)



class Podcasts(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def searchPodcast(self, search_string:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("podcasts.searchPodcast", **args)
		return PodcastsSearchPodcastResponse(**r)



class Polls(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addVote(self, owner_id:Optional[int]=None, poll_id:Optional[int]=None, answer_ids:Optional[list]=None, is_board:Optional[bool]=None):
		"""Adds the current user's vote to the selected answer in the poll."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.addVote", **args)
		return PollsAddVoteResponse(**r)


	async def create(self, question:Optional[str]=None, is_anonymous:Optional[bool]=None, is_multiple:Optional[bool]=None, end_date:Optional[int]=None, owner_id:Optional[int]=None, app_id:Optional[int]=None, add_answers:Optional[str]=None, photo_id:Optional[int]=None, background_id:Optional[str]=None, disable_unvote:Optional[bool]=None):
		"""Creates polls that can be attached to the users' or communities' posts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.create", **args)
		return PollsCreateResponse(**r)


	async def deleteVote(self, owner_id:Optional[int]=None, poll_id:Optional[int]=None, answer_id:Optional[int]=None, is_board:Optional[bool]=None):
		"""Deletes the current user's vote from the selected answer in the poll."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.deleteVote", **args)
		return PollsDeleteVoteResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, poll_id:Optional[int]=None, question:Optional[str]=None, add_answers:Optional[str]=None, edit_answers:Optional[str]=None, delete_answers:Optional[str]=None, end_date:Optional[int]=None, photo_id:Optional[int]=None, background_id:Optional[str]=None):
		"""Edits created polls"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.edit", **args)
		return BaseOkResponse(**r)


	async def getBackgrounds(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.getBackgrounds", **args)
		return PollsGetBackgroundsResponse.parse_obj(r)


	async def getById(self, owner_id:Optional[int]=None, is_board:Optional[bool]=None, poll_id:Optional[int]=None, extended:Optional[bool]=None, friends_count:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns detailed information about a poll by its ID."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.getById", **args)
		return PollsGetByIdResponse(**r)


	async def getPhotoUploadServer(self, owner_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.getPhotoUploadServer", **args)
		return BaseGetUploadServerResponse(**r)


	async def getVoters(self, owner_id:Optional[int]=None, poll_id:Optional[int]=None, answer_ids:Optional[list]=None, is_board:Optional[bool]=None, friends_only:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns a list of IDs of users who selected specific answers in the poll."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.getVoters", **args)
		return PollsGetVotersResponse.parse_obj(r)


	async def savePhoto(self, photo:Optional[str]=None, hash:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("polls.savePhoto", **args)
		return PollsSavePhotoResponse(**r)



class Prettycards(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def create(self, owner_id:Optional[int]=None, photo:Optional[str]=None, title:Optional[str]=None, link:Optional[str]=None, price:Optional[str]=None, price_old:Optional[str]=None, button:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.create", **args)
		return PrettyCardsCreateResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, card_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.delete", **args)
		return PrettyCardsDeleteResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, card_id:Optional[int]=None, photo:Optional[str]=None, title:Optional[str]=None, link:Optional[str]=None, price:Optional[str]=None, price_old:Optional[str]=None, button:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.edit", **args)
		return PrettyCardsEditResponse(**r)


	async def get(self, owner_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.get", **args)
		return PrettyCardsGetResponse(**r)


	async def getById(self, owner_id:Optional[int]=None, card_ids:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.getById", **args)
		return PrettyCardsGetByIdResponse.parse_obj(r)


	async def getUploadURL(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("prettycards.getUploadURL", **args)
		return PrettyCardsGetUploadURLResponse(**r)



class Search(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getHints(self, q:Optional[str]=None, offset:Optional[int]=None, limit:Optional[int]=None, filters:Optional[list]=None, fields:Optional[list]=None, search_global:Optional[bool]=None):
		"""Allows the programmer to do a quick search for any substring."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("search.getHints", **args)
		return SearchGetHintsResponse(**r)



class Secure(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addAppEvent(self, user_id:Optional[int]=None, activity_id:Optional[int]=None, value:Optional[int]=None):
		"""Adds user activity information to an application"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.addAppEvent", **args)
		return BaseOkResponse(**r)


	async def checkToken(self, token:Optional[str]=None, ip:Optional[str]=None):
		"""Checks the user authentication in 'IFrame' and 'Flash' apps using the 'access_token' parameter."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.checkToken", **args)
		return SecureCheckTokenResponse(**r)


	async def getAppBalance(self):
		"""Returns payment balance of the application in hundredth of a vote."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.getAppBalance", **args)
		return SecureGetAppBalanceResponse(**r)


	async def getSMSHistory(self, user_id:Optional[int]=None, date_from:Optional[int]=None, date_to:Optional[int]=None, limit:Optional[int]=None):
		"""Shows a list of SMS notifications sent by the application using [vk.com/dev/secure.sendSMSNotification|secure.sendSMSNotification] method."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.getSMSHistory", **args)
		return SecureGetSMSHistoryResponse.parse_obj(r)


	async def getTransactionsHistory(self, type:Optional[int]=None, uid_from:Optional[int]=None, uid_to:Optional[int]=None, date_from:Optional[int]=None, date_to:Optional[int]=None, limit:Optional[int]=None):
		"""Shows history of votes transaction between users and the application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.getTransactionsHistory", **args)
		return SecureGetTransactionsHistoryResponse.parse_obj(r)


	async def getUserLevel(self, user_ids:Optional[list]=None):
		"""Returns one of the previously set game levels of one or more users in the application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.getUserLevel", **args)
		return SecureGetUserLevelResponse.parse_obj(r)


	async def giveEventSticker(self, user_ids:Optional[list]=None, achievement_id:Optional[int]=None):
		"""Opens the game achievement and gives the user a sticker"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.giveEventSticker", **args)
		return SecureGiveEventStickerResponse.parse_obj(r)


	async def sendNotification(self, user_ids:Optional[list]=None, user_id:Optional[int]=None, message:Optional[str]=None):
		"""Sends notification to the user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.sendNotification", **args)
		return SecureSendNotificationResponse.parse_obj(r)


	async def sendSMSNotification(self, user_id:Optional[int]=None, message:Optional[str]=None):
		"""Sends 'SMS' notification to a user's mobile device."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.sendSMSNotification", **args)
		return BaseOkResponse(**r)


	async def setCounter(self, counters:Optional[list]=None, user_id:Optional[int]=None, counter:Optional[int]=None, increment:Optional[bool]=None):
		"""Sets a counter which is shown to the user in bold in the left menu."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("secure.setCounter", **args)
		for i in [BaseBoolResponse, SecureSetCounterArrayResponse]:
			try: return i(**r)
			except: return BaseBoolResponse(**r)



class Stats(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, group_id:Optional[int]=None, app_id:Optional[int]=None, timestamp_from:Optional[int]=None, timestamp_to:Optional[int]=None, interval:Optional[str]=None, intervals_count:Optional[int]=None, filters:Optional[list]=None, stats_groups:Optional[list]=None, extended:Optional[bool]=None):
		"""Returns statistics of a community or an application."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stats.get", **args)
		return StatsGetResponse.parse_obj(r)


	async def getPostReach(self, owner_id:Optional[str]=None, post_ids:Optional[list]=None):
		"""Returns stats for a wall post."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stats.getPostReach", **args)
		return StatsGetPostReachResponse.parse_obj(r)


	async def trackVisitor(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stats.trackVisitor", **args)
		return BaseOkResponse(**r)



class Status(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, user_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Returns data required to show the status of a user or community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("status.get", **args)
		return StatusGetResponse(**r)


	async def set(self, text:Optional[str]=None, group_id:Optional[int]=None):
		"""Sets a new status for the current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("status.set", **args)
		return BaseOkResponse(**r)



class Storage(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, key:Optional[str]=None, keys:Optional[list]=None, user_id:Optional[int]=None):
		"""Returns a value of variable with the name set by key parameter."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("storage.get", **args)
		return StorageGetResponse.parse_obj(r)


	async def getKeys(self, user_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns the names of all variables."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("storage.getKeys", **args)
		return StorageGetKeysResponse.parse_obj(r)


	async def set(self, key:Optional[str]=None, value:Optional[str]=None, user_id:Optional[int]=None):
		"""Saves a value of variable with the name set by 'key' parameter."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("storage.set", **args)
		return BaseOkResponse(**r)



class Store(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def addStickersToFavorite(self, sticker_ids:Optional[list]=None):
		"""Adds given sticker IDs to the list of user's favorite stickers"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("store.addStickersToFavorite", **args)
		return BaseOkResponse(**r)


	async def getFavoriteStickers(self):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("store.getFavoriteStickers", **args)
		return StoreGetFavoriteStickersResponse.parse_obj(r)


	async def getProducts(self, type:Optional[str]=None, merchant:Optional[str]=None, section:Optional[str]=None, product_ids:Optional[list]=None, filters:Optional[list]=None, extended:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("store.getProducts", **args)
		return StoreGetProductsResponse.parse_obj(r)


	async def getStickersKeywords(self, stickers_ids:Optional[list]=None, products_ids:Optional[list]=None, aliases:Optional[bool]=None, all_products:Optional[bool]=None, need_stickers:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("store.getStickersKeywords", **args)
		return StoreGetStickersKeywordsResponse(**r)


	async def removeStickersFromFavorite(self, sticker_ids:Optional[list]=None):
		"""Removes given sticker IDs from the list of user's favorite stickers"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("store.removeStickersFromFavorite", **args)
		return BaseOkResponse(**r)



class Stories(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def banOwner(self, owners_ids:Optional[list]=None):
		"""Allows to hide stories from chosen sources from current user's feed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.banOwner", **args)
		return BaseOkResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, story_id:Optional[int]=None, stories:Optional[list]=None):
		"""Allows to delete story."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.delete", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns stories available for current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.get", **args)
		return StoriesGetV5113Response(**r)


	async def getBanned(self, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns list of sources hidden from current user's feed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getBanned", **args)
		for i in [StoriesGetBannedResponse, StoriesGetBannedExtendedResponse]:
			try: return i(**r)
			except: return StoriesGetBannedResponse(**r)


	async def getById(self, stories:Optional[list]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns story by its ID."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getById", **args)
		return StoriesGetByIdExtendedResponse(**r)


	async def getPhotoUploadServer(self, add_to_news:Optional[bool]=None, user_ids:Optional[list]=None, reply_to_story:Optional[str]=None, link_text:Optional[str]=None, link_url:Optional[str]=None, group_id:Optional[int]=None, clickable_stickers:Optional[str]=None):
		"""Returns URL for uploading a story with photo."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getPhotoUploadServer", **args)
		return StoriesGetPhotoUploadServerResponse(**r)


	async def getReplies(self, owner_id:Optional[int]=None, story_id:Optional[int]=None, access_key:Optional[str]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns replies to the story."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getReplies", **args)
		return StoriesGetV5113Response(**r)


	async def getStats(self, owner_id:Optional[int]=None, story_id:Optional[int]=None):
		"""Returns stories available for current user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getStats", **args)
		return StoriesGetStatsResponse(**r)


	async def getVideoUploadServer(self, add_to_news:Optional[bool]=None, user_ids:Optional[list]=None, reply_to_story:Optional[str]=None, link_text:Optional[str]=None, link_url:Optional[str]=None, group_id:Optional[int]=None, clickable_stickers:Optional[str]=None):
		"""Allows to receive URL for uploading story with video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getVideoUploadServer", **args)
		return StoriesGetVideoUploadServerResponse(**r)


	async def getViewers(self, owner_id:Optional[int]=None, story_id:Optional[int]=None, count:Optional[int]=None, offset:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns a list of story viewers."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.getViewers", **args)
		for i in [StoriesGetViewersExtendedV5115Response, StoriesGetViewersExtendedV5115Response]:
			try: return i(**r)
			except: return StoriesGetViewersExtendedV5115Response(**r)


	async def hideAllReplies(self, owner_id:Optional[int]=None, group_id:Optional[int]=None):
		"""Hides all replies in the last 24 hours from the user to current user's stories."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.hideAllReplies", **args)
		return BaseOkResponse(**r)


	async def hideReply(self, owner_id:Optional[int]=None, story_id:Optional[int]=None):
		"""Hides the reply to the current user's story."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.hideReply", **args)
		return BaseOkResponse(**r)


	async def save(self, upload_results:Optional[list]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.save", **args)
		return StoriesSaveResponse(**r)


	async def search(self, q:Optional[str]=None, place_id:Optional[int]=None, latitude:Optional[int]=None, longitude:Optional[int]=None, radius:Optional[int]=None, mentioned_id:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.search", **args)
		return StoriesGetV5113Response(**r)


	async def sendInteraction(self, access_key:Optional[str]=None, message:Optional[str]=None, is_broadcast:Optional[bool]=None, is_anonymous:Optional[bool]=None, unseen_marker:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.sendInteraction", **args)
		return BaseOkResponse(**r)


	async def unbanOwner(self, owners_ids:Optional[list]=None):
		"""Allows to show stories from hidden sources in current user's feed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("stories.unbanOwner", **args)
		return BaseOkResponse(**r)



class Streaming(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getServerUrl(self):
		"""Allows to receive data for the connection to Streaming API."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("streaming.getServerUrl", **args)
		return StreamingGetServerUrlResponse(**r)


	async def setSettings(self, monthly_tier:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("streaming.setSettings", **args)
		return BaseOkResponse(**r)



class Users(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def get(self, user_ids:Optional[list]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns detailed information on users."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("users.get", **args)
		return UsersGetResponse.parse_obj(r)


	async def getFollowers(self, user_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, name_case:Optional[str]=None):
		"""Returns a list of IDs of followers of the user in question, sorted by date added, most recent first."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("users.getFollowers", **args)
		for i in [UsersGetFollowersResponse, UsersGetFollowersFieldsResponse]:
			try: return i(**r)
			except: return UsersGetFollowersResponse(**r)


	async def getSubscriptions(self, user_id:Optional[int]=None, extended:Optional[bool]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None):
		"""Returns a list of IDs of users and communities followed by the user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("users.getSubscriptions", **args)
		for i in [UsersGetSubscriptionsResponse, UsersGetSubscriptionsExtendedResponse]:
			try: return i(**r)
			except: return UsersGetSubscriptionsResponse(**r)


	async def report(self, user_id:Optional[int]=None, type:Optional[str]=None, comment:Optional[str]=None):
		"""Reports (submits a complain about) a user."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("users.report", **args)
		return BaseOkResponse(**r)


	async def search(self, q:Optional[str]=None, sort:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, fields:Optional[list]=None, city:Optional[int]=None, country:Optional[int]=None, hometown:Optional[str]=None, university_country:Optional[int]=None, university:Optional[int]=None, university_year:Optional[int]=None, university_faculty:Optional[int]=None, university_chair:Optional[int]=None, sex:Optional[int]=None, status:Optional[int]=None, age_from:Optional[int]=None, age_to:Optional[int]=None, birth_day:Optional[int]=None, birth_month:Optional[int]=None, birth_year:Optional[int]=None, online:Optional[bool]=None, has_photo:Optional[bool]=None, school_country:Optional[int]=None, school_city:Optional[int]=None, school_class:Optional[int]=None, school:Optional[int]=None, school_year:Optional[int]=None, religion:Optional[str]=None, company:Optional[str]=None, position:Optional[str]=None, group_id:Optional[int]=None, from_list:Optional[list]=None):
		"""Returns a list of users matching the search criteria."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("users.search", **args)
		return UsersSearchResponse(**r)



class Utils(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def checkLink(self, url:Optional[str]=None):
		"""Checks whether a link is blocked in VK."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.checkLink", **args)
		return UtilsCheckLinkResponse(**r)


	async def deleteFromLastShortened(self, key:Optional[str]=None):
		"""Deletes shortened link from user's list."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.deleteFromLastShortened", **args)
		return BaseOkResponse(**r)


	async def getLastShortenedLinks(self, count:Optional[int]=None, offset:Optional[int]=None):
		"""Returns a list of user's shortened links."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.getLastShortenedLinks", **args)
		return UtilsGetLastShortenedLinksResponse(**r)


	async def getLinkStats(self, key:Optional[str]=None, source:Optional[str]=None, access_key:Optional[str]=None, interval:Optional[str]=None, intervals_count:Optional[int]=None, extended:Optional[bool]=None):
		"""Returns stats data for shortened link."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.getLinkStats", **args)
		for i in [UtilsGetLinkStatsResponse, UtilsGetLinkStatsExtendedResponse]:
			try: return i(**r)
			except: return UtilsGetLinkStatsResponse(**r)


	async def getServerTime(self):
		"""Returns the current time of the VK server."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.getServerTime", **args)
		return UtilsGetServerTimeResponse(**r)


	async def getShortLink(self, url:Optional[str]=None, private:Optional[bool]=None):
		"""Allows to receive a link shortened via vk.cc."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.getShortLink", **args)
		return UtilsGetShortLinkResponse(**r)


	async def resolveScreenName(self, screen_name:Optional[str]=None):
		"""Detects a type of object (e.g., user, community, application) and its ID by screen name."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("utils.resolveScreenName", **args)
		return UtilsResolveScreenNameResponse(**r)



class Video(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def add(self, target_id:Optional[int]=None, video_id:Optional[int]=None, owner_id:Optional[int]=None):
		"""Adds a video to a user or community page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.add", **args)
		return BaseOkResponse(**r)


	async def addAlbum(self, group_id:Optional[int]=None, title:Optional[str]=None, privacy:Optional[list]=None):
		"""Creates an empty album for videos."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.addAlbum", **args)
		return VideoAddAlbumResponse(**r)


	async def addToAlbum(self, target_id:Optional[int]=None, album_id:Optional[int]=None, album_ids:Optional[list]=None, owner_id:Optional[int]=None, video_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.addToAlbum", **args)
		for i in [BaseOkResponse, VideoChangeVideoAlbumsResponse]:
			try: return i(**r)
			except: return BaseOkResponse(**r)


	async def createComment(self, owner_id:Optional[int]=None, video_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, from_group:Optional[bool]=None, reply_to_comment:Optional[int]=None, sticker_id:Optional[int]=None, guid:Optional[str]=None):
		"""Adds a new comment on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.createComment", **args)
		return VideoCreateCommentResponse(**r)


	async def delete(self, video_id:Optional[int]=None, owner_id:Optional[int]=None, target_id:Optional[int]=None):
		"""Deletes a video from a user or community page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.delete", **args)
		return BaseOkResponse(**r)


	async def deleteAlbum(self, group_id:Optional[int]=None, album_id:Optional[int]=None):
		"""Deletes a video album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.deleteAlbum", **args)
		return BaseOkResponse(**r)


	async def deleteComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Deletes a comment on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.deleteComment", **args)
		return BaseOkResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, video_id:Optional[int]=None, name:Optional[str]=None, desc:Optional[str]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None, no_comments:Optional[bool]=None, repeat:Optional[bool]=None):
		"""Edits information about a video on a user or community page."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.edit", **args)
		return BaseOkResponse(**r)


	async def editAlbum(self, group_id:Optional[int]=None, album_id:Optional[int]=None, title:Optional[str]=None, privacy:Optional[list]=None):
		"""Edits the title of a video album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.editAlbum", **args)
		return BaseOkResponse(**r)


	async def editComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None):
		"""Edits the text of a comment on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.editComment", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, videos:Optional[list]=None, album_id:Optional[int]=None, count:Optional[int]=None, offset:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns detailed information about videos."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.get", **args)
		return VideoGetResponse(**r)


	async def getAlbumById(self, owner_id:Optional[int]=None, album_id:Optional[int]=None):
		"""Returns video album info"""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.getAlbumById", **args)
		return VideoGetAlbumByIdResponse(**r)


	async def getAlbums(self, owner_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None, need_system:Optional[bool]=None):
		"""Returns a list of video albums owned by a user or community."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.getAlbums", **args)
		for i in [VideoGetAlbumsResponse, VideoGetAlbumsExtendedResponse]:
			try: return i(**r)
			except: return VideoGetAlbumsResponse(**r)


	async def getAlbumsByVideo(self, target_id:Optional[int]=None, owner_id:Optional[int]=None, video_id:Optional[int]=None, extended:Optional[bool]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.getAlbumsByVideo", **args)
		for i in [VideoGetAlbumsByVideoResponse, VideoGetAlbumsByVideoExtendedResponse]:
			try: return i(**r)
			except: return VideoGetAlbumsByVideoResponse(**r)


	async def getComments(self, owner_id:Optional[int]=None, video_id:Optional[int]=None, need_likes:Optional[bool]=None, start_comment_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, sort:Optional[str]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns a list of comments on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.getComments", **args)
		for i in [VideoGetCommentsResponse, VideoGetCommentsExtendedResponse]:
			try: return i(**r)
			except: return VideoGetCommentsResponse(**r)


	async def removeFromAlbum(self, target_id:Optional[int]=None, album_id:Optional[int]=None, album_ids:Optional[list]=None, owner_id:Optional[int]=None, video_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.removeFromAlbum", **args)
		for i in [BaseOkResponse, VideoChangeVideoAlbumsResponse]:
			try: return i(**r)
			except: return BaseOkResponse(**r)


	async def reorderAlbums(self, owner_id:Optional[int]=None, album_id:Optional[int]=None, before:Optional[int]=None, after:Optional[int]=None):
		"""Reorders the album in the list of user video albums."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.reorderAlbums", **args)
		return BaseOkResponse(**r)


	async def reorderVideos(self, target_id:Optional[int]=None, album_id:Optional[int]=None, owner_id:Optional[int]=None, video_id:Optional[int]=None, before_owner_id:Optional[int]=None, before_video_id:Optional[int]=None, after_owner_id:Optional[int]=None, after_video_id:Optional[int]=None):
		"""Reorders the video in the video album."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.reorderVideos", **args)
		return BaseOkResponse(**r)


	async def report(self, owner_id:Optional[int]=None, video_id:Optional[int]=None, reason:Optional[int]=None, comment:Optional[str]=None, search_query:Optional[str]=None):
		"""Reports (submits a complaint about) a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.report", **args)
		return BaseOkResponse(**r)


	async def reportComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, reason:Optional[int]=None):
		"""Reports (submits a complaint about) a comment on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.reportComment", **args)
		return BaseOkResponse(**r)


	async def restore(self, video_id:Optional[int]=None, owner_id:Optional[int]=None):
		"""Restores a previously deleted video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.restore", **args)
		return BaseOkResponse(**r)


	async def restoreComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Restores a previously deleted comment on a video."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.restoreComment", **args)
		return VideoRestoreCommentResponse(**r)


	async def save(self, name:Optional[str]=None, description:Optional[str]=None, is_private:Optional[bool]=None, wallpost:Optional[bool]=None, link:Optional[str]=None, group_id:Optional[int]=None, album_id:Optional[int]=None, privacy_view:Optional[list]=None, privacy_comment:Optional[list]=None, no_comments:Optional[bool]=None, repeat:Optional[bool]=None, compression:Optional[bool]=None):
		"""Returns a server address (required for upload) and video data."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.save", **args)
		return VideoSaveResponse(**r)


	async def search(self, q:Optional[str]=None, sort:Optional[int]=None, hd:Optional[int]=None, adult:Optional[bool]=None, live:Optional[bool]=None, filters:Optional[list]=None, search_own:Optional[bool]=None, offset:Optional[int]=None, longer:Optional[int]=None, shorter:Optional[int]=None, count:Optional[int]=None, extended:Optional[bool]=None):
		"""Returns a list of videos under the set search criterion."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("video.search", **args)
		for i in [VideoSearchResponse, VideoSearchExtendedResponse]:
			try: return i(**r)
			except: return VideoSearchResponse(**r)



class Wall(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def checkCopyrightLink(self, link:Optional[str]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.checkCopyrightLink", **args)
		return BaseBoolResponse(**r)


	async def closeComments(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.closeComments", **args)
		return BaseBoolResponse(**r)


	async def createComment(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, from_group:Optional[int]=None, message:Optional[str]=None, reply_to_comment:Optional[int]=None, attachments:Optional[list]=None, sticker_id:Optional[int]=None, guid:Optional[str]=None):
		"""Adds a comment to a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.createComment", **args)
		return WallCreateCommentResponse(**r)


	async def delete(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		"""Deletes a post from a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.delete", **args)
		return BaseOkResponse(**r)


	async def deleteComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Deletes a comment on a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.deleteComment", **args)
		return BaseOkResponse(**r)


	async def edit(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, friends_only:Optional[bool]=None, message:Optional[str]=None, attachments:Optional[list]=None, services:Optional[str]=None, signed:Optional[bool]=None, publish_date:Optional[int]=None, lat:Optional[int]=None, long:Optional[int]=None, place_id:Optional[int]=None, mark_as_ads:Optional[bool]=None, close_comments:Optional[bool]=None, donut_paid_duration:Optional[int]=None, poster_bkg_id:Optional[int]=None, poster_bkg_owner_id:Optional[int]=None, poster_bkg_access_hash:Optional[str]=None, copyright:Optional[str]=None, topic_id:Optional[int]=None):
		"""Edits a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.edit", **args)
		return WallEditResponse(**r)


	async def editAdsStealth(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, signed:Optional[bool]=None, lat:Optional[int]=None, long:Optional[int]=None, place_id:Optional[int]=None, link_button:Optional[str]=None, link_title:Optional[str]=None, link_image:Optional[str]=None, link_video:Optional[str]=None):
		"""Allows to edit hidden post."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.editAdsStealth", **args)
		return BaseOkResponse(**r)


	async def editComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None):
		"""Edits a comment on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.editComment", **args)
		return BaseOkResponse(**r)


	async def get(self, owner_id:Optional[int]=None, domain:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None, filter:Optional[str]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns a list of posts on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.get", **args)
		for i in [WallGetResponse, WallGetExtendedResponse]:
			try: return i(**r)
			except: return WallGetResponse(**r)


	async def getById(self, posts:Optional[list]=None, extended:Optional[bool]=None, copy_history_depth:Optional[int]=None, fields:Optional[list]=None):
		"""Returns a list of posts from user or community walls by their IDs."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.getById", **args)
		for i in [WallGetByIdLegacyResponse, WallGetByIdExtendedResponse]:
			try: return i(**r)
			except: return WallGetByIdLegacyResponse(**r)


	async def getComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Returns a comment on a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.getComment", **args)
		for i in [WallGetCommentResponse, WallGetCommentExtendedResponse]:
			try: return i(**r)
			except: return WallGetCommentResponse(**r)


	async def getComments(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, need_likes:Optional[bool]=None, start_comment_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None, sort:Optional[str]=None, preview_length:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None, comment_id:Optional[int]=None, thread_items_count:Optional[int]=None):
		"""Returns a list of comments on a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.getComments", **args)
		for i in [WallGetCommentsResponse, WallGetCommentsExtendedResponse]:
			try: return i(**r)
			except: return WallGetCommentsResponse(**r)


	async def getReposts(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Returns information about reposts of a post on user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.getReposts", **args)
		return WallGetRepostsResponse(**r)


	async def openComments(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.openComments", **args)
		return BaseBoolResponse(**r)


	async def pin(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		"""Pins the post on wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.pin", **args)
		return BaseOkResponse(**r)


	async def post(self, owner_id:Optional[int]=None, friends_only:Optional[bool]=None, from_group:Optional[bool]=None, message:Optional[str]=None, attachments:Optional[list]=None, services:Optional[str]=None, signed:Optional[bool]=None, publish_date:Optional[int]=None, lat:Optional[int]=None, long:Optional[int]=None, place_id:Optional[int]=None, post_id:Optional[int]=None, guid:Optional[str]=None, mark_as_ads:Optional[bool]=None, close_comments:Optional[bool]=None, donut_paid_duration:Optional[int]=None, mute_notifications:Optional[bool]=None, copyright:Optional[str]=None, topic_id:Optional[int]=None):
		"""Adds a new post on a user wall or community wall. Can also be used to publish suggested or scheduled posts."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.post", **args)
		return WallPostResponse(**r)


	async def postAdsStealth(self, owner_id:Optional[int]=None, message:Optional[str]=None, attachments:Optional[list]=None, signed:Optional[bool]=None, lat:Optional[int]=None, long:Optional[int]=None, place_id:Optional[int]=None, guid:Optional[str]=None, link_button:Optional[str]=None, link_title:Optional[str]=None, link_image:Optional[str]=None, link_video:Optional[str]=None):
		"""Allows to create hidden post which will not be shown on the community's wall and can be used for creating an ad with type 'Community post'."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.postAdsStealth", **args)
		return WallPostAdsStealthResponse(**r)


	async def reportComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None, reason:Optional[int]=None):
		"""Reports (submits a complaint about) a comment on a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.reportComment", **args)
		return BaseOkResponse(**r)


	async def reportPost(self, owner_id:Optional[int]=None, post_id:Optional[int]=None, reason:Optional[int]=None):
		"""Reports (submits a complaint about) a post on a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.reportPost", **args)
		return BaseOkResponse(**r)


	async def repost(self, object:Optional[str]=None, message:Optional[str]=None, group_id:Optional[int]=None, mark_as_ads:Optional[bool]=None, mute_notifications:Optional[bool]=None):
		"""Reposts (copies) an object to a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.repost", **args)
		return WallRepostResponse(**r)


	async def restore(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		"""Restores a post deleted from a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.restore", **args)
		return BaseOkResponse(**r)


	async def restoreComment(self, owner_id:Optional[int]=None, comment_id:Optional[int]=None):
		"""Restores a comment deleted from a user wall or community wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.restoreComment", **args)
		return BaseOkResponse(**r)


	async def search(self, owner_id:Optional[int]=None, domain:Optional[str]=None, query:Optional[str]=None, owners_only:Optional[bool]=None, count:Optional[int]=None, offset:Optional[int]=None, extended:Optional[bool]=None, fields:Optional[list]=None):
		"""Allows to search posts on user or community walls."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.search", **args)
		for i in [WallSearchResponse, WallSearchExtendedResponse]:
			try: return i(**r)
			except: return WallSearchResponse(**r)


	async def unpin(self, owner_id:Optional[int]=None, post_id:Optional[int]=None):
		"""Unpins the post on wall."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("wall.unpin", **args)
		return BaseOkResponse(**r)



class Widgets(BaseMethod):
	def __init__(self, vk):
		super().__init__(vk)

	async def getComments(self, widget_api_id:Optional[int]=None, url:Optional[str]=None, page_id:Optional[str]=None, order:Optional[str]=None, fields:Optional[list]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Gets a list of comments for the page added through the [vk.com/dev/Comments|Comments widget]."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("widgets.getComments", **args)
		return WidgetsGetCommentsResponse(**r)


	async def getPages(self, widget_api_id:Optional[int]=None, order:Optional[str]=None, period:Optional[str]=None, offset:Optional[int]=None, count:Optional[int]=None):
		"""Gets a list of application/site pages where the [vk.com/dev/Comments|Comments widget] or [vk.com/dev/Like|Like widget] is installed."""
		args = locals()
		for i in ('self', '__class__'): args.pop(i)
		r = await super()._method("widgets.getPages", **args)
		return WidgetsGetPagesResponse(**r)


__all__ =('Account', 'Ads', 'Adsweb', 'Appwidgets', 'Apps', 'Auth', 'Board', 'Database', 'Docs', 'Donut', 
          'Downloadedgames', 'Fave', 'Friends','Gifts', 'Groups', 'Leadforms', 'Likes', 'Market', 
          'Messages', 'Newsfeed', 'Notes', 'Notifications', 'Orders', 'Pages', 'Photos',
          'Podcasts', 'Polls', 'Prettycards', 'Search', 'Secure', 'Stats', 'Status', 'Storage', 'Store', 
          'Stories', 'Streaming', 'Users', 'Utils', 'Video', 'Wall', 'Widgets')
