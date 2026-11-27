# 200 use cases for one person

Everything Sam Rivera might hand to a personal agent in a year, from the morning brief to filing taxes. Each folder has a `usecase.py` (a framework-neutral spec) and a README with the flow. The same spec runs on LangChain Deep Agents, LangGraph, Google ADK or the Claude Agent SDK, whichever the user picked.

Features used: approval (75), parallel calls (73), memory (58), uses preferences (48), guard (17).

## Mornings and daily planning (1-20)

| # | Use case | You ask | Features |
|---|---|---|---|
| 1 | [Morning brief](001_morning_brief/) | Give me my morning brief. | parallel calls, uses preferences |
| 2 | [Commute check](002_commute_check/) | How's my commute looking? | parallel calls, uses preferences |
| 3 | [Plan my day from my task list](003_day_plan_from_tasks/) | Plan my day around my meetings. | parallel calls, memory, uses preferences |
| 4 | [Wake-up routine](004_wake_up_routine/) | Run my wake-up routine. | parallel calls, guard |
| 5 | [What should I wear](005_what_to_wear/) | What should I wear today? | parallel calls, uses preferences |
| 6 | [School run check](006_school_run_check/) | Anything I need for Maya's school today? | parallel calls, memory, uses preferences |
| 7 | [News digest on my topics](007_news_digest_by_topic/) | Summarize the news for my topics. | parallel calls, uses preferences |
| 8 | [Overnight inbox triage](008_inbox_zero_triage/) | Triage my overnight email. | approval |
| 9 | [Daily reminders setup](009_medication_reminder_setup/) | Set my usual daily reminders. | parallel calls, memory, uses preferences |
| 10 | [Birthdays coming up](010_birthday_check/) | Any birthdays this week? | approval |
| 11 | [Focus mode until noon](011_focus_mode/) | Turn on focus mode until noon. | parallel calls, approval |
| 12 | [Breakfast from what's in the fridge](012_breakfast_idea/) | What can I make for breakfast? | uses preferences |
| 13 | [Street cleaning check](013_parking_reminder/) | Do I need to move my car today? | memory, uses preferences |
| 14 | [Habit tracker check-in](014_habit_streak/) | Log that I meditated and show my streaks. |  |
| 15 | [Packages arriving today](015_package_tracking/) | Are any packages coming today? | parallel calls |
| 16 | [Is it OK to run outside](016_air_quality_run/) | Can I run outside this morning? | parallel calls, memory, uses preferences |
| 17 | [Out-of-office for a sick day](017_set_out_of_office/) | I'm out sick today. Handle it. | parallel calls, approval |
| 18 | [Today's one goal](018_daily_quote_and_goal/) | Remember my one goal for today: finish the report draft. | memory |
| 19 | [Evening review](019_evening_review/) | Do my evening review. | parallel calls, memory |
| 20 | [Sunday week-ahead plan](020_weekly_plan_sunday/) | Plan my week. | parallel calls, memory |

## Email, messages and calendar (21-40)

| # | Use case | You ask | Features |
|---|---|---|---|
| 21 | [Draft replies to important email](021_reply_drafts/) | Draft replies to the emails that need me. | parallel calls, approval |
| 22 | [Find a time and book a meeting](022_schedule_meeting/) | Book an hour with Priya and Tom next week. | approval |
| 23 | [Unsubscribe from junk](023_unsubscribe_cleanup/) | Unsubscribe me from newsletters I never open. | parallel calls, approval |
| 24 | [Summarize a meeting transcript](024_meeting_notes_summary/) | Summarize the budget meeting and list my action items. |  |
| 25 | [Follow-ups I'm waiting on](025_follow_up_nudges/) | Who hasn't replied to me this week? | approval |
| 26 | [Calendar conflicts](026_calendar_conflicts/) | Any double bookings this week? | parallel calls, uses preferences |
| 27 | [Decline a meeting politely](027_decline_politely/) | Decline Friday's optional all-hands and say why. | approval, memory |
| 28 | [Catch up on the family group chat](028_group_chat_catchup/) | What did I miss in the family chat? |  |
| 29 | [Save a new contact from an email](029_save_contact_details/) | Save the plumber from that email as a contact. | memory |
| 30 | [Who emails me most](030_weekly_email_report/) | Who takes most of my email time? |  |
| 31 | [Make an email filter](031_create_email_filter/) | Filter project-alerts into a folder. | approval, guard |
| 32 | [RSVP to a party](032_rsvp_party/) | RSVP yes to the Chens' party for me and Jordan. | approval, uses preferences |
| 33 | [Meeting across time zones](033_time_zone_meeting/) | Find a time for a call with my cousin in Madrid. | uses preferences |
| 34 | [Voicemails to text](034_voicemail_transcribe/) | What are my voicemails about? |  |
| 35 | [Share an event with family](035_share_calendar_family/) | Add Maya's recital to Jordan's calendar too. | approval, uses preferences |
| 36 | [Is this email phishing?](036_phishing_check/) | Is the 'your account is locked' email real? |  |
| 37 | [Thank-you notes after a party](037_thank_you_notes/) | Draft thank-you notes for Maya's birthday gifts. | parallel calls, approval, memory |
| 38 | [Reschedule an appointment](038_reschedule_dentist/) | Move my dentist appointment to next week. | parallel calls, approval |
| 39 | [Remember how I like to reply](039_auto_reply_rules/) | Remember: keep my replies short and sign off with just 'Sam'. | memory |
| 40 | [Clear out stale recurring meetings](040_weekly_calendar_cleanup/) | Which recurring meetings could I drop? | parallel calls, approval |

## Bills, budget and money admin (41-60)

| # | Use case | You ask | Features |
|---|---|---|---|
| 41 | [Bills due this week](041_bills_due_this_week/) | What bills are due this week? | parallel calls |
| 42 | [Pay a bill (with a spending limit)](042_pay_bill_with_limit/) | Pay the electric bill and the Visa. | parallel calls, approval, guard |
| 43 | [Monthly budget review](043_monthly_budget_review/) | How did I do against my budget this month? | parallel calls |
| 44 | [Subscription audit](044_subscription_audit/) | What subscriptions am I paying for? | approval |
| 45 | [Split a dinner bill](045_split_dinner_bill/) | Split last night's $186 dinner four ways and request payment. | parallel calls, approval |
| 46 | [Check an unusual charge](046_unusual_charge_check/) | What's this $89 charge from 'SQ *BLUEDOOR'? |  |
| 47 | [Savings goal progress](047_savings_goal_progress/) | How's the vacation fund coming along? | parallel calls, memory |
| 48 | [Move money to savings](048_move_money_to_savings/) | Move $500 to savings. | approval |
| 49 | [Tax documents checklist](049_tax_documents_checklist/) | Which tax documents do I still need? | parallel calls, memory |
| 50 | [Price drop after I bought it](050_price_drop_refund/) | Did anything I bought recently drop in price? | approval |
| 51 | [Set up rent autopay](051_rent_reminder_autopay/) | Set up rent autopay for the 1st. | approval, guard |
| 52 | [Credit report alerts](052_credit_score_check/) | Any changes on my credit report? |  |
| 53 | [How much is that in dollars](053_currency_for_trip/) | Convert 250 euros for my trip budget. | uses preferences |
| 54 | [Collect donation receipts](054_donation_receipts/) | Gather my donation receipts for the year. | memory |
| 55 | [Compare insurance renewal quotes](055_insurance_renewal_compare/) | My car insurance renews next month. Is it a good price? | parallel calls |
| 56 | [Buy a new laptop](056_big_purchase_blocked/) | Buy the laptop in my cart. | approval, guard |
| 57 | [Send an invoice for side work](057_invoice_freelance/) | Invoice Bright Co for 6 hours of design work. | approval, memory |
| 58 | [Set a dining spending alert](058_set_spending_alert/) | Alert me if dining goes over $250 this month. | memory |
| 59 | [Household expenses with Jordan](059_shared_expenses/) | What do Jordan and I owe each other this month? | approval, uses preferences |
| 60 | [Year-end money summary](060_year_end_money_summary/) | Give me my money summary for the year. | parallel calls |

## Shopping, groceries and errands (61-80)

| # | Use case | You ask | Features |
|---|---|---|---|
| 61 | [Grocery list from this week's meals](061_grocery_list_from_meals/) | Make my grocery list for this week's meal plan. | parallel calls, memory, uses preferences |
| 62 | [Order groceries for delivery](062_order_groceries/) | Order my grocery list for Saturday morning delivery. | parallel calls, approval, guard, memory |
| 63 | [Find the best price](063_price_compare/) | Where's the cheapest place to buy a 65-inch TV? | parallel calls |
| 64 | [Start a return](064_return_an_item/) | Return the shoes that don't fit. | approval |
| 65 | [Pharmacy pickup check](065_pharmacy_pickup/) | Is my prescription ready? |  |
| 66 | [Book a haircut](066_book_haircut/) | Book my usual haircut next week. | approval, memory |
| 67 | [Dry cleaning reminder](067_dry_cleaning_reminder/) | Remind me to pick up dry cleaning when I'm near it. |  |
| 68 | [Gift ideas](068_gift_ideas/) | Gift ideas for Jordan's birthday under $100? | memory |
| 69 | [Buy and ship a gift](069_buy_gift/) | Order the trail running vest, gift wrapped. | approval, guard |
| 70 | [Book a car service](070_car_service/) | My car is due for an oil change. Book it. | parallel calls, approval |
| 71 | [Library books due](071_library_books/) | Any library books due? |  |
| 72 | [Restock household basics](072_restock_household/) | Restock the usual household stuff. | parallel calls, approval, memory |
| 73 | [What's open near me](073_find_open_now/) | Is the hardware store open now? | uses preferences |
| 74 | [Batch my errands into one trip](074_post_office_trip/) | I need the post office, pharmacy and hardware store. Best route? | uses preferences |
| 75 | [Is it still under warranty](075_warranty_lookup/) | Is the dishwasher still under warranty? |  |
| 76 | [Hire help for a task](076_furniture_assembly/) | Find someone to assemble a bookshelf this weekend. | approval |
| 77 | [Farmers market this weekend](077_farmers_market/) | What's at the farmers market this weekend? | parallel calls, uses preferences |
| 78 | [Schedule a donation pickup](078_donate_clothes/) | Schedule a pickup for two bags of clothes. | approval |
| 79 | [Coupons before I check out](079_coupon_finder/) | Any coupons for my HomeMart cart? |  |
| 80 | [Weekly errand list](080_weekly_errand_list/) | Save this week's errands: post office, return shoes, pick up dry cleaning. | memory |

## Travel and getting around (81-100)

| # | Use case | You ask | Features |
|---|---|---|---|
| 81 | [Weekend trip ideas](081_weekend_trip_ideas/) | Ideas for a weekend away within 4 hours' drive? | parallel calls, uses preferences |
| 82 | [Find flights](082_flight_search/) | Find flights to Denver for Dec 12-15. | uses preferences |
| 83 | [Book the flight](083_book_flight_limit/) | Book the United flight to Denver. | approval, guard |
| 84 | [Hotel shortlist](084_hotel_shortlist/) | Hotels near the conference center in Denver under $200? |  |
| 85 | [Packing list](085_packing_list/) | Make a packing list for Denver. | parallel calls, memory |
| 86 | [Flight check-in](086_check_in_reminder/) | Check me in for tomorrow's flight. | approval, uses preferences |
| 87 | [My flight is delayed](087_flight_delay_rebook/) | My flight is delayed 3 hours. Options? | parallel calls, approval |
| 88 | [Ride to the airport](088_airport_ride/) | Get me to O'Hare by 6am tomorrow. | parallel calls, approval, uses preferences |
| 89 | [File trip expenses](089_expense_trip_receipts/) | File my Denver trip expenses. | approval |
| 90 | [Passport expiry check](090_passport_expiry/) | Is my passport OK for Spain next spring? | parallel calls, memory |
| 91 | [Road trip stops](091_road_trip_stops/) | Plan stops for the drive to Nashville with the dog. | uses preferences |
| 92 | [Travel money setup](092_currency_and_cards/) | Set up my card for the Spain trip. | approval |
| 93 | [Trip itinerary to calendar](093_itinerary_to_calendar/) | Put my Denver itinerary on my calendar. | parallel calls |
| 94 | [Dinner near my hotel](094_local_recs/) | Good vegetarian dinner near the Maven? | uses preferences |
| 95 | [Do I need a visa](095_visa_requirements/) | Do I need a visa for a week in Japan? |  |
| 96 | [Book a pet sitter](096_pet_sitter/) | Book a sitter for Biscuit while I'm in Denver. | approval, memory, uses preferences |
| 97 | [Points and miles check](097_loyalty_points/) | How many points do I have, and are any expiring? | parallel calls |
| 98 | [Cheaper commute](098_commute_alternatives/) | Would biking to work save me money? | parallel calls, uses preferences |
| 99 | [Remember my travel preferences](099_save_travel_prefs/) | Remember: aisle seat, no red-eyes, carry-on only. | memory |
| 100 | [Trip recap](100_trip_recap/) | Recap the Denver trip: cost and what I'd do again. | memory |

## Home, family and pets (101-120)

| # | Use case | You ask | Features |
|---|---|---|---|
| 101 | [Set the thermostat schedule](101_thermostat_schedule/) | Set the heat to 68 when we're home, 60 at night. | guard |
| 102 | [Weekly chore rotation](102_chore_rotation/) | Make this week's chore rotation and send it to the family. | approval, memory, uses preferences |
| 103 | [Vet appointment for the dog](103_vet_appointment/) | Biscuit is due for vaccines. Book the vet. | parallel calls, approval, uses preferences |
| 104 | [Home maintenance calendar](104_maintenance_reminders/) | What home maintenance is due? | parallel calls |
| 105 | [Homework check](105_kid_homework_check/) | Does Maya have homework due tomorrow? | uses preferences |
| 106 | [Plan family dinners](106_family_dinner_plan/) | Plan dinners for the week that Maya will actually eat. | memory, uses preferences |
| 107 | [Book a babysitter](107_babysitter_booking/) | Book a sitter for Saturday 6-11pm. | approval |
| 108 | [Guest access for the dog walker](108_smart_lock_guest/) | Give the dog walker a door code for weekdays at noon. | approval, guard |
| 109 | [Why is the electric bill high](109_energy_usage/) | Why was the electric bill high this month? | parallel calls |
| 110 | [Get the plumber in](110_plumber_quote/) | The kitchen sink is leaking. Get the plumber. | approval, memory |
| 111 | [Shared shopping list](111_grocery_with_partner/) | Add oat milk and coffee to the list Jordan and I share. |  |
| 112 | [Sign Maya up for swim class](112_kid_activity_signup/) | Sign Maya up for the Saturday swim class. | approval, guard, uses preferences |
| 113 | [Where did I leave my keys](113_lost_item_finder/) | Where are my keys? |  |
| 114 | [Make a photo album](114_family_photos_album/) | Make an album of Thanksgiving photos and share it with family. | approval |
| 115 | [Dog food running low](115_dog_food_reorder/) | Are we low on dog food? | approval, uses preferences |
| 116 | [Who came to the door](116_security_camera_review/) | Who came to the door today? |  |
| 117 | [Family week overview](117_family_calendar_week/) | What's the family doing this week? | parallel calls, uses preferences |
| 118 | [Kid allowance](118_allowance_tracker/) | Pay Maya's weekly allowance. | approval, uses preferences |
| 119 | [Start an insurance claim](119_renters_insurance_claim/) | The leak damaged the cabinet. Start a claim. | approval |
| 120 | [Remember family details](120_remember_family_details/) | Remember: Maya likes cheese and pasta, hates mushrooms. | memory |

## Fitness, food and appointments (121-140)

| # | Use case | You ask | Features |
|---|---|---|---|
| 121 | [This week's workouts](121_workout_plan_week/) | Plan my workouts around my calendar. | parallel calls, memory |
| 122 | [Book a gym class](122_book_gym_class/) | Book a spin class for Wednesday evening. | approval |
| 123 | [Running progress](123_running_progress/) | How's my running going this month? | parallel calls |
| 124 | [Sunday meal prep](124_meal_prep_sunday/) | Plan a meal prep for weekday lunches. | uses preferences |
| 125 | [Drink-water reminders](125_water_reminder/) | Remind me to drink water every 2 hours during work. | uses preferences |
| 126 | [Prep for a doctor's appointment](126_doctor_appointment_prep/) | Help me prepare for my checkup on Friday. | parallel calls, memory |
| 127 | [Save questions for the doctor](127_save_doctor_questions/) | Note for my checkup: ask about knee pain when running. | memory |
| 128 | [Sleep summary](128_sleep_summary/) | How have I been sleeping? |  |
| 129 | [Restaurant that fits my diet](129_restaurant_for_diet/) | Dinner spot for 4 tonight, something everyone can eat. | approval, uses preferences |
| 130 | [Step challenge with friends](130_steps_challenge/) | Start a 7-day step challenge with Lee and Ana. | approval |
| 131 | [Refill a prescription](131_prescription_refill/) | Refill my usual prescription. | approval |
| 132 | [Log what I ate](132_calorie_free_food_log/) | Log lunch: lentil soup and bread. |  |
| 133 | [Sign up for a 10K](133_race_signup/) | Sign me up for the spring 10K. | approval |
| 134 | [Physio exercise reminders](134_physio_exercises/) | Remind me to do my physio exercises every evening. | memory |
| 135 | [Weekly wellness summary](135_weekly_health_summary/) | Give me my week: sleep, steps, workouts. | parallel calls |
| 136 | [Book a dental cleaning](136_dentist_cleaning/) | When was my last cleaning? Book the next one. | parallel calls, approval |
| 137 | [Order healthy snacks for the office](137_healthy_snacks_order/) | Order snacks for my desk. | approval, guard |
| 138 | [Screen time check](138_screen_time/) | How much time did I spend on my phone this week? | approval |
| 139 | [Turn a call into a walk](139_walking_meeting/) | Make my 3pm call a walking meeting if the weather's OK. | approval, uses preferences |
| 140 | [Set a fitness goal](140_save_fitness_goal/) | My goal: run a 10K under 55 minutes by April. | memory |

## Work and career (141-160)

| # | Use case | You ask | Features |
|---|---|---|---|
| 141 | [Draft my standup update](141_standup_update/) | Draft my standup update. | parallel calls, memory |
| 142 | [Weekly status report](142_weekly_status_report/) | Write my weekly status report and send it to my manager. | approval |
| 143 | [Prep for my 1:1](143_prep_one_on_one/) | Prep my 1:1 with my manager. | parallel calls, memory |
| 144 | [Save a 1:1 topic](144_save_1on1_topic/) | For my next 1:1: ask about the training budget. | memory |
| 145 | [Summarize a long document](145_document_summary/) | Summarize the 40-page vendor contract. |  |
| 146 | [Outline a presentation](146_presentation_outline/) | Outline a 10-minute talk on our Q4 results. | memory |
| 147 | [What's my role worth](147_job_market_check/) | What are similar roles paying in my city? | uses preferences |
| 148 | [Add a win to my resume](148_update_resume/) | Add the quarterly report project to my resume. | approval |
| 149 | [Follow up after a conference](149_networking_follow_up/) | Follow up with the people I met at the conference. | parallel calls, approval, memory |
| 150 | [Request time off](150_pto_request/) | Request PTO for April 3-13. | parallel calls, approval |
| 151 | [Use the learning budget](151_learning_budget_course/) | Enroll me in the data analysis course with my learning budget. | approval, guard |
| 152 | [Block focus time](152_focus_time_blocks/) | Block 2 hours of focus time each morning next week. | parallel calls |
| 153 | [Catch up on Slack after a day off](153_slack_catchup/) | What did I miss on Slack yesterday? |  |
| 154 | [Submit a lunch receipt](154_expense_receipt_snap/) | Submit yesterday's client lunch receipt. | approval, guard |
| 155 | [Schedule interviews](155_interview_scheduling/) | Schedule 3 candidate interviews for next week. | parallel calls, approval |
| 156 | [Check my goals](156_okr_check/) | Where am I on my quarterly goals? |  |
| 157 | [Translate a message](157_translate_message/) | Translate my reply to the Madrid team into Spanish. | approval |
| 158 | [Which meetings cost the most time](158_meeting_cost/) | Which meetings take most of my week? |  |
| 159 | [End-of-day shutdown](159_end_of_day_shutdown/) | Shut down my workday. | parallel calls, memory |
| 160 | [Brag doc entry](160_career_notes/) | Add to my brag doc: led the Q4 review across 4 teams. | memory |

## Learning and hobbies (161-180)

| # | Use case | You ask | Features |
|---|---|---|---|
| 161 | [Daily Spanish practice](161_daily_language_practice/) | Give me today's Spanish practice. | memory |
| 162 | [What should I read next](162_reading_list/) | What should I read next? | parallel calls, memory |
| 163 | [Place a library hold](163_place_library_hold/) | Put Klara and the Sun on hold. | approval |
| 164 | [Online course progress](164_course_progress/) | How far am I in the data analysis course? |  |
| 165 | [Study schedule](165_study_schedule/) | Put my course study sessions on the calendar. | parallel calls |
| 166 | [Guitar practice log](166_guitar_practice_log/) | Log 30 minutes of guitar: worked on barre chords. |  |
| 167 | [Podcasts for my commute](167_podcast_queue/) | Queue podcasts for tomorrow's commute. | uses preferences |
| 168 | [Museum visit this weekend](168_museum_visit/) | Any good exhibits this weekend, and free days? | parallel calls, uses preferences |
| 169 | [Concert tickets](169_buy_concert_tickets/) | Get 2 tickets for the jazz show Friday. | approval, guard |
| 170 | [Photo spots at sunset](170_photography_tips/) | Where should I take sunset photos this week? | parallel calls, uses preferences |
| 171 | [Plan the spring garden](171_garden_plan/) | What should I plant this spring? | memory |
| 172 | [Book club prep](172_book_club_summary/) | Prep me for book club: questions on Sea of Tranquility. | memory |
| 173 | [Side project: what's next](173_coding_side_project/) | What's next on my side project? | parallel calls, memory |
| 174 | [Book a cooking class](174_cooking_class/) | Book a pasta-making class for Jordan and me. | approval, uses preferences |
| 175 | [Daily chess puzzle](175_chess_puzzle_daily/) | Give me today's chess puzzle at my level. | memory |
| 176 | [Sign up to volunteer](176_volunteer_shift/) | Find a volunteer shift this month and sign me up. | approval, uses preferences |
| 177 | [Word of the day](177_word_of_the_day/) | Teach me a useful word today. | memory |
| 178 | [Hobby spending](178_hobby_budget/) | How much did I spend on hobbies this year? |  |
| 179 | [Remember books I liked](179_save_book_taste/) | Remember I loved The Overstory and Project Hail Mary. | memory |
| 180 | [Monthly learning review](180_monthly_learning_review/) | What did I learn this month? | parallel calls, memory |

## Documents, accounts and digital life (181-200)

| # | Use case | You ask | Features |
|---|---|---|---|
| 181 | [Were any of my accounts breached?](181_password_breach_check/) | Check if my email showed up in a data breach. |  |
| 182 | [Are my backups working](182_backup_check/) | Did my laptop and phone back up this week? | parallel calls |
| 183 | [Free up cloud storage](183_free_up_storage/) | My cloud storage is full. Clean it up. | parallel calls, approval, guard |
| 184 | [Find a document](184_document_finder/) | Find my car title document. |  |
| 185 | [Document renewal dates](185_id_renewal_reminders/) | When do my license and passport need renewing? | parallel calls, memory |
| 186 | [Save expiry dates](186_save_expiry_dates/) | My license expires March 2027, passport June 2027. | memory |
| 187 | [Scan and file a letter](187_scan_and_file/) | File the insurance letter I just scanned. |  |
| 188 | [Which accounts lack 2FA](188_two_factor_audit/) | Which of my important accounts don't have 2FA? |  |
| 189 | [Clean up blurry photos](189_photo_cleanup/) | Find blurry and duplicate photos from this month. |  |
| 190 | [Why is the Wi-Fi slow](190_wifi_troubleshoot/) | The Wi-Fi is slow. What's wrong? | approval |
| 191 | [New phone checklist](191_new_phone_setup/) | I got a new phone. What do I need to move over? | parallel calls, memory |
| 192 | [Close an old account](192_cancel_unused_account/) | Delete my OldForum account. | approval |
| 193 | [Share a document safely](193_share_document_safely/) | Share my lease with the new landlord. | approval, guard |
| 194 | [Leaving-home routine](194_smart_home_routine/) | Run my leaving-home routine. | parallel calls |
| 195 | [Register a new purchase's warranty](195_warranty_registry/) | Register the warranty for the new TV. | approval |
| 196 | [Save email attachments](196_email_attachments_to_drive/) | Save all the school PDFs from email to the Maya folder. | parallel calls, uses preferences |
| 197 | [Update a card on file](197_subscription_password_update/) | My card was replaced. Which services have the old one? |  |
| 198 | [Monthly digital declutter](198_digital_declutter/) | Do my monthly digital declutter. | parallel calls |
| 199 | [Emergency contact sheet](199_emergency_contacts/) | Make an emergency contact sheet for the babysitter. | parallel calls, memory, uses preferences |
| 200 | [My year in review](200_year_in_review/) | Give me my year in review. | parallel calls, memory |
